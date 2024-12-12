from django.core.management.base import BaseCommand
from archive.models import Conference
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Command(BaseCommand):
    help = 'PDF 회의록 URL을 확인합니다'

    def handle(self, *args, **options):
        # Chrome 드라이버 설정
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # 헤드리스 모드 해제
        options.add_argument('--start-maximized')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            # 첫 번째 회의록만 테스트
            conf = Conference.objects.first()
            self.stdout.write(f"회의록 ID: {conf.회의록ID}")
            self.stdout.write(f"원본 URL: {conf.회의록URL}")
            
            # conferNum과 fileId 추출
            confer_num = conf.회의록URL.split('conferNum=')[1].split('&')[0]
            file_id = conf.회의록URL.split('fileId=')[1]
            
            # 뷰어 URL 구성 시도
            viewer_url = f"https://likms.assembly.go.kr/record/new/viewRecord.jsp?conferNum={confer_num}&fileId={file_id}"
            
            self.stdout.write(f"\n뷰어 URL 시도: {viewer_url}")
            
            # 페이지 로드
            driver.get(viewer_url)
            time.sleep(5)  # 페이지 로딩 대기
            
            # 페이지 소스 확인
            self.stdout.write("\n페이지 소스 일부:")
            source = driver.page_source
            self.stdout.write(source[:1000])  # 처음 1000자만 출력
            
            # iframe 찾기
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            self.stdout.write(f"\n발견된 iframe 수: {len(iframes)}")
            
            for idx, iframe in enumerate(iframes):
                self.stdout.write(f"\niframe {idx + 1}:")
                self.stdout.write(f"src: {iframe.get_attribute('src')}")
                self.stdout.write(f"id: {iframe.get_attribute('id')}")
                self.stdout.write(f"name: {iframe.get_attribute('name')}")
            
            # 스크린샷 저장 (디버깅용)
            driver.save_screenshot("viewer_page.png")
            self.stdout.write("\n스크린샷이 저장되었습니다: viewer_page.png")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'오류 발생: {str(e)}'))
        finally:
            time.sleep(3)  # 결과 확인을 위한 대기
            driver.quit()