from django.core.management.base import BaseCommand
from django.db.models import Count
from archive.api_client import AssemblyAPI
from archive.models import AssemblyMember
from tqdm import tqdm

class Command(BaseCommand):
    help = '국회의원 정보를 업데이트합니다.'

    def handle(self, *args, **options):
        try:
            print("국회의원 정보를 가져오는 중...")
            
            api = AssemblyAPI()
            members = api.get_assembly_members()
            
            print(f"\nAPI에서 받아온 데이터 수: {len(members)}")
            
            # 첫 번째 데이터 출력해서 확인
            if members:
                print("\n첫 번째 의원 데이터 샘플:")
                print(members[0])
            
            # 기존 데이터 삭제
            AssemblyMember.objects.all().delete()
            
            # 새로운 데이터 저장
            print("\n의원 정보 저장 중...")
            success_count = 0
            error_count = 0
            
            for member in tqdm(members):
                try:
                    AssemblyMember.objects.create(
                        의원코드=member['id'],
                        이름=member['이름'],
                        한자이름=member['한자이름'],
                        영문이름=member['영문이름'],
                        생년월일=member['생년월일'],
                        직책=member['직책'],
                        정당=member['정당'],
                        선거구=member['선거구'],
                        선거구구분=member['선거구구분'],
                        위원회=member['위원회'],
                        소속위원회=member['소속위원회'],
                        당선횟수=member['당선횟수'],
                        당선대수=member['당선대수'],
                        성별=member['성별'],
                        전화번호=member['전화번호'],
                        이메일=member['이메일'],
                        홈페이지=member['홈페이지'],
                        보좌관=member['보좌관'],
                        비서관=member['비서관'],
                        비서=member['비서'],
                        약력=member['약력'],
                        사무실호실=member['사무실호실'],
                        사진=member['사진']
                    )
                    success_count += 1
                except Exception as e:
                    print(f"\n데이터 저장 중 오류 발생: {str(e)}")
                    print(f"문제가 된 데이터: {member}")
                    error_count += 1
            
            print(f"\n== 처리 결과 ==")
            print(f"성공: {success_count}건")
            print(f"실패: {error_count}건")
            
            print("\n== 정당별 의원 수 ==")
            party_counts = AssemblyMember.objects.values('정당').annotate(count=Count('id'))
            for party in party_counts:
                print(f"{party['정당'] or '무소속'}: {party['count']}명")
                
        except Exception as e:
            print(f"\n전체 처리 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())