from django.core.management.base import BaseCommand
from archive.crawlers import AssemblyMemberCrawler
from archive.models import Politician
from tqdm import tqdm

class Command(BaseCommand):
    help = '현직 국회의원 명단을 크롤링하여 데이터베이스에 저장합니다'

    def handle(self, *args, **options):
        crawler = AssemblyMemberCrawler()
        
        self.stdout.write("국회의원 명단을 크롤링 중...")
        members = crawler.crawl_members()
        
        with tqdm(total=len(members), desc="의원 정보 저장 중") as pbar:
            for member in members:
                # 이미 존재하는 의원인지 확인
                politician, created = Politician.objects.get_or_create(
                    name=member['name'],
                    defaults={
                        'party': member['party'],
                        'position': member['position']
                    }
                )
                
                if not created:
                    # 기존 의원의 정당 정보 업데이트
                    politician.party = member['party']
                    politician.save()
                
                pbar.update(1)
        
        self.stdout.write(self.style.SUCCESS(f'총 {len(members)}명의 국회의원 정보가 저장되었습니다!')) 