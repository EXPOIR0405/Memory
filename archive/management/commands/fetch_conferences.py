from django.core.management.base import BaseCommand
from django.conf import settings
from archive.clients.assembly_api import AssemblyOpenAPI
from archive.models import Conference
from datetime import datetime
from tqdm import tqdm

class Command(BaseCommand):
    help = '국회 회의록 목록을 가져옵니다'

    def handle(self, *args, **options):
        api = AssemblyOpenAPI(settings.ASSEMBLY_API_KEY)
        
        # 22대 국회 데이터 가져오기
        era_code = "22"
        
        self.stdout.write("회의록 목록을 가져오는 중...")
        conferences = api.get_all_conference_list(era_code)
        
        if not conferences:
            self.stdout.write(self.style.WARNING("데이터를 가져오지 못했습니다."))
            return
            
        self.stdout.write(f"총 {len(conferences)}개의 회의록을 처리합니다...")
        
        success_count = 0
        error_count = 0
        
        with tqdm(total=len(conferences)) as pbar:
            for conf in conferences:
                try:
                    # 날짜 형식 변환 (YYYY-MM-DD 형식으로)
                    date_str = conf['CONF_DT']
                    if len(date_str) == 8:  # YYYYMMDD 형식인 경우
                        conf_date = datetime.strptime(date_str, '%Y%m%d').date()
                    else:  # YYYY-MM-DD 형식인 경우
                        conf_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    Conference.objects.update_or_create(
                        회의록ID=conf['CONF_ID'],
                        defaults={
                            '대수': conf['ERACO'],
                            '회기': conf['SESS'],
                            '차수': conf['DGR'],
                            '회의일자': conf_date,
                            '회의종류': conf['CONF_KND'],
                            '위원회코드': conf['CMIT_CD'],
                            '위원회명': conf['CMIT_NM'],
                            '회의록URL': conf['DOWN_URL']
                        }
                    )
                    success_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing conference: {str(e)}'))
                    self.stdout.write(self.style.ERROR(f'Problem data: {conf}'))
                    error_count += 1
                
                pbar.update(1)
        
        self.stdout.write(self.style.SUCCESS(f'\n처리 완료:'))
        self.stdout.write(f'성공: {success_count}개')
        self.stdout.write(f'실패: {error_count}개')