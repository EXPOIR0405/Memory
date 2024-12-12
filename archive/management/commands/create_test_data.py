from django.core.management.base import BaseCommand
from django.utils import timezone
from archive.models import Conference, AssemblyMember, SpeechRecord
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = '테스트용 회의록 및 발언 데이터를 생성합니다'

    def handle(self, *args, **options):
        try:
            # 테스트용 의원 데이터 생성
            self.stdout.write("테스트 의원 데이터 생성 중...")
            members = [
                {
                    "이름": "홍길동",
                    "정당": "더불어민주당",
                    "선거구": "서울 강남구갑",
                    "당선횟수": "3"
                },
                {
                    "이름": "김철수",
                    "정당": "국민의힘",
                    "선거구": "부산 해운대구을",
                    "당선횟수": "2"
                },
                {
                    "이름": "이영희",
                    "정당": "정의당",
                    "선거구": "비례대표",
                    "당선횟수": "1"
                }
            ]
            
            created_members = []
            for member_data in members:
                member, created = AssemblyMember.objects.get_or_create(
                    이름=member_data["이름"],
                    defaults=member_data
                )
                created_members.append(member)
                if created:
                    self.stdout.write(f"의원 생성됨: {member.이름}")
            
            # 테스트용 회의록 데이터 생성
            self.stdout.write("\n테스트 회의록 데이터 생성 중...")
            base_date = timezone.now().date()
            conferences = [
                {
                    "회의록ID": "TEST001",
                    "대수": "22",
                    "회기": "1",
                    "차수": "1",
                    "회의일자": base_date - timedelta(days=5),
                    "회의종류": "본회의",
                    "위원회코드": "9999",
                    "위원회명": "국회본회의",
                    "회의록URL": "http://example.com/test1"
                },
                {
                    "회의록ID": "TEST002",
                    "대수": "22",
                    "회기": "1",
                    "차수": "1",
                    "회의일자": base_date - timedelta(days=3),
                    "회의종류": "상임위",
                    "위원회코드": "2000",
                    "위원회명": "정무위원회",
                    "회의록URL": "http://example.com/test2"
                }
            ]
            
            created_conferences = []
            for conf_data in conferences:
                conference, created = Conference.objects.get_or_create(
                    회의록ID=conf_data["회의록ID"],
                    defaults=conf_data
                )
                created_conferences.append(conference)
                if created:
                    self.stdout.write(f"회의록 생성됨: {conference.회의록ID}")
            
            # 테스트용 발언 데이터 생성
            self.stdout.write("\n테스트 발언 데이터 생성 중...")
            speeches = [
                {
                    "conference": created_conferences[0],
                    "assembly_member": created_members[0],
                    "content": "예산 심의와 관련하여 말씀드리겠습니다. 이번 추경예산안은 면밀한 검토가 필요합니다.",
                    "speech_order": 1
                },
                {
                    "conference": created_conferences[0],
                    "assembly_member": created_members[1],
                    "content": "복지예산 증액에 대해 신중한 접근이 필요하다고 생각합니다.",
                    "speech_order": 2
                },
                {
                    "conference": created_conferences[1],
                    "assembly_member": created_members[2],
                    "content": "기후변화 대응을 위한 예산 편성을 제안합니다.",
                    "speech_order": 1
                }
            ]
            
            for speech_data in speeches:
                speech, created = SpeechRecord.objects.get_or_create(
                    conference=speech_data["conference"],
                    assembly_member=speech_data["assembly_member"],
                    speech_order=speech_data["speech_order"],
                    defaults={"content": speech_data["content"]}
                )
                if created:
                    self.stdout.write(f"발언 생성됨: {speech.assembly_member.이름}의 발언")
            
            self.stdout.write(self.style.SUCCESS("\n테스트 데이터 생성 완료!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'오류 발생: {str(e)}')) 