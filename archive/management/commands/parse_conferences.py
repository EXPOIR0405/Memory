from django.core.management.base import BaseCommand
from archive.models import Conference, ConferenceContent
from archive.parsers.conference_parser import ConferenceParser
from tqdm import tqdm

class Command(BaseCommand):
    help = '회의록 파일을 다운로드하고 파싱합니다'

    def handle(self, *args, **options):
        parser = ConferenceParser()
        
        # 아직 내용이 파싱되지 않은 회의록만 가져옵니다
        conferences = Conference.objects.filter(conferencecontent__isnull=True)
        
        self.stdout.write(f"총 {conferences.count()}개의 회의록을 처리합니다...")
        
        with tqdm(total=conferences.count()) as pbar:
            for conference in conferences:
                try:
                    content = parser.parse_conference(conference.download_url)
                    ConferenceContent.objects.create(
                        conference=conference,
                        content=content
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'회의록 {conference.conference_id} 처리 중 오류 발생: {str(e)}'
                    ))
                
                pbar.update(1)
        
        self.stdout.write(self.style.SUCCESS('회의록 파싱이 완료되었습니다!')) 