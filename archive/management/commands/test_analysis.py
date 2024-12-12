from django.core.management.base import BaseCommand
from archive.services.analysis_service import ConferenceAnalyzer
from archive.services.alert_service import AlertService
from archive.models import SpeechRecord, KeywordAlert
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = '회의록 분석 및 알림 시스템 테스트'

    def handle(self, *args, **options):
        # 분석 테스트
        analyzer = ConferenceAnalyzer()
        
        # 키워드 검색 테스트
        self.stdout.write("키워드 검색 테스트 중...")
        keyword = "예산"
        results = analyzer.search_keyword(keyword)
        self.stdout.write(f"'{keyword}' 키워드 검색 결과: {results.count()}건")
        
        # 발언 통계 테스트
        self.stdout.write("\n발언 통계 테스트 중...")
        stats = analyzer.get_member_speech_stats()
        for stat in stats[:5]:  # 상위 5개만 출력
            self.stdout.write(f"{stat['assembly_member__이름']}: {stat['speech_count']}회")
        
        # 알림 테스트
        self.stdout.write("\n알림 시스템 테스트 중...")
        try:
            # 테스트용 사용자 생성 또는 업데이트
            user, created = User.objects.update_or_create(
                username='test_user',
                defaults={
                    'email': 'rkdalswjd0405@gmail.com',
                    'is_active': True
                }
            )
            
            # 테스트용 키워드 알림 생성
            keyword_alert, created = KeywordAlert.objects.get_or_create(
                user=user,
                keyword='예산'
            )
            
            # 가장 최근 발언으로 알림 테스트
            recent_speech = SpeechRecord.objects.first()
            if recent_speech:
                AlertService.check_keyword_alerts(recent_speech)
                self.stdout.write("알림 이메일 발송 완료!")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'오류 발생: {str(e)}')) 