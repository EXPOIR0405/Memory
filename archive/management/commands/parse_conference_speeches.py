from django.core.management.base import BaseCommand
from archive.models import Conference, SpeechRecord, AssemblyMember
import re
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Command(BaseCommand):
    help = '회의록 내용을 파싱하여 발언 기록을 저장합니다'

    def handle(self, *args, **options):
        # Chrome 드라이버 설정
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 브라우저 창 안보이게 실행
        driver = webdriver.Chrome(options=options)
        
        # 파싱되지 않은 회의록 가져오기
        conferences = Conference.objects.filter(conferencecontent__isnull=True)
        
        self.stdout.write(f"총 {conferences.count()}개의 회의록을 처리합니다...")
        
        success_count = 0
        error_count = 0
        
        try:
            for conf in tqdm(conferences):
                try:
                    # URL이 유효한지 확인
                    if not conf.회의록URL or 'likms.assembly.go.kr' not in conf.회의록URL:
                        self.stdout.write(f"잘못된 URL 형식: {conf.회의록ID}")
                        error_count += 1
                        continue

                    # 페이지 로드
                    driver.get(conf.회의록URL)
                    
                    # 회의록 내용이 로드될 때까지 대기 (최대 10초)
                    try:
                        content_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'record_read'))
                        )
                        time.sleep(2)  # 추가 대기 시간
                        content = content_element.text
                    except Exception as e:
                        self.stdout.write(f"내용 로딩 실패 ({conf.회의록ID}): {str(e)}")
                        error_count += 1
                        continue

                    if not content:
                        self.stdout.write(f"내용이 비어있음: {conf.회의록ID}")
                        error_count += 1
                        continue

                    # 발언 패턴 (예: ◯홍길동 의원 또는 ◯위원장 홍길동)
                    pattern = r'◯([가-힣]+\s*(?:의원|위원장|위원|장관|총리|대통령)|\s*[가-힣]+)'
                    
                    # 발언 분리
                    parts = re.split(pattern, content)
                    if len(parts) > 1:
                        for i in range(1, len(parts), 2):
                            speaker = parts[i].strip()
                            speech_content = parts[i+1].strip() if i+1 < len(parts) else ""
                            
                            # 발언자 이름 추출
                            name_match = re.search(r'([가-힣]+)', speaker)
                            if name_match:
                                speaker_name = name_match.group(1)
                                
                                try:
                                    member = AssemblyMember.objects.get(이름__contains=speaker_name)
                                    
                                    # 발언 저장
                                    if speech_content:
                                        SpeechRecord.objects.create(
                                            conference=conf,
                                            assembly_member=member,
                                            content=speech_content,
                                            speech_order=i//2 + 1
                                        )
                                except AssemblyMember.DoesNotExist:
                                    self.stdout.write(f"미등록 발언자: {speaker_name}")
                                    continue
                                except AssemblyMember.MultipleObjectsReturned:
                                    self.stdout.write(f"중복된 발언자: {speaker_name}")
                                    continue

                    success_count += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'회의록 처리 중 오류 발생 ({conf.회의록ID}): {str(e)}'))
                    error_count += 1
                    continue
                
        finally:
            driver.quit()  # 브라우저 종료

        self.stdout.write(self.style.SUCCESS(f'\n처리 완료:'))
        self.stdout.write(f'성공: {success_count}개')
        self.stdout.write(f'실패: {error_count}개')