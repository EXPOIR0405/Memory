from django.core.management.base import BaseCommand
from archive.crawlers import NewsCrawler
from tqdm import tqdm
import time

class Command(BaseCommand):
    help = '정치인들의 발언을 크롤링합니다'

    def handle(self, *args, **options):
        crawler = NewsCrawler()
        from archive.models import Politician
        politicians = Politician.objects.all()
        
        # 전체 진행 상황을 보여주는 프로그레스 바
        with tqdm(total=len(politicians), desc="전체 진행률", unit="명") as pbar:
            for politician in politicians:
                self.stdout.write(f"\n{politician.name}의 발언을 크롤링 중...")
                
                # 각 정치인별 크롤링 진행 상황을 보여주는 프로그레스 바
                statements = []
                expected_pages = 10  # 예상 페이지 수
                
                with tqdm(total=expected_pages, desc=f"{politician.name} 크롤링", 
                         unit="page", leave=False) as page_bar:
                    for page in range(expected_pages):
                        # 여기서 실제 크롤링 수행
                        page_statements = crawler.crawl_news(politician.name, page=page)
                        statements.extend(page_statements)
                        
                        # 페이지별 진행 상황 업데이트
                        page_bar.update(1)
                        time.sleep(0.5)  # 서버 부하 방지를 위한 딜레이
                
                # 크롤링한 데이터 저장
                crawler.save_statements(politician.name, statements)
                
                # 전체 진행 상황 업데이트
                pbar.update(1)
        
        self.stdout.write(self.style.SUCCESS('\n크롤링이 완료되었습니다!')) 