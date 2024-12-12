from django.core.management.base import BaseCommand
from archive.models import Conference

class Command(BaseCommand):
    help = '테스트 데이터를 제거합니다'

    def handle(self, *args, **options):
        # example.com을 포함하는 테스트 데이터 삭제
        test_conferences = Conference.objects.filter(회의록URL__contains='example.com')
        count = test_conferences.count()
        test_conferences.delete()
        
        self.stdout.write(f"테스트 데이터 {count}개가 삭제되었습니다.")
        
        # 남은 실제 회의록 확인
        remaining = Conference.objects.all()
        self.stdout.write(f"남은 실제 회의록: {remaining.count()}개")
        
        # 샘플로 첫 5개 회의록 정보 출력
        self.stdout.write("\n실제 회의록 샘플:")
        for conf in remaining[:5]:
            self.stdout.write(f"ID: {conf.회의록ID}")
            self.stdout.write(f"URL: {conf.회의록URL}")
            self.stdout.write("-" * 50) 