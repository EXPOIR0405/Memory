from django.core.management.base import BaseCommand
from archive.models import Conference

class Command(BaseCommand):
    help = '데이터베이스에 저장된 회의록 URL들을 확인합니다'

    def handle(self, *args, **options):
        conferences = Conference.objects.all()
        self.stdout.write(f"총 회의록 수: {conferences.count()}")
        
        self.stdout.write("\n첫 10개 회의록 URL 확인:")
        for conf in conferences[:10]:
            self.stdout.write(f"ID: {conf.회의록ID}")
            self.stdout.write(f"URL: {conf.회의록URL}")
            self.stdout.write("-" * 50) 