from django.core.management.base import BaseCommand
from archive.models import Conference, SpeechRecord, AssemblyMember
import requests
import tempfile
import os
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import easyocr
from pdf2image import convert_from_path
import re
import numpy as np

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.reader = easyocr.Reader(['ko'])  # 한글 OCR 리더 초기화
        self.stdout.write("EasyOCR 초기화 완료...")

    def extract_speeches(self, pdf_path):
        """PDF에서 발언 내용을 추출"""
        try:
            # Poppler 경로 지정
            poppler_path = r"C:\Program Files\Release-24.08.0-0\poppler-24.08.0\Library\bin"
            
            # PDF를 이미지로 변환
            images = convert_from_path(
                pdf_path,
                poppler_path=poppler_path
            )
            
            self.stdout.write(f"PDF 변환 완료: {len(images)}페이지")
            
            full_text = ""
            for i, image in enumerate(images, 1):
                self.stdout.write(f"페이지 {i} OCR 처리 중...")
                # PIL Image를 numpy 배열로 변환
                image_np = np.array(image)
                
                # EasyOCR로 텍스트 추출
                results = self.reader.readtext(image_np)
                page_text = ' '.join([text[1] for text in results])
                full_text += page_text + "\n"
                
                # 첫 페이지 OCR 결과 샘플 출력
                if i == 1:
                    self.stdout.write("\nOCR 결과 샘플:")
                    self.stdout.write(page_text[:500])
                    self.stdout.write("\n" + "="*50 + "\n")
            
            # 발언 패턴 찾기
            patterns = [
                r'◯\s*([가-힣]+\s*(?:의원|위원장|위원|장관|총리|대통령)|\s*[가-힣]+)\s*([^◯]+)',
                r'○\s*([가-힣]+\s*(?:의원|위원장|위원|장관|총리|대통령)|\s*[가-힣]+)\s*([^○]+)',
                r'0\s*([가-힣]+\s*(?:의원|위원장|위원|장관|총리|대통령)|\s*[가-힣]+)\s*([^0]+)',
            ]
            
            speeches = []
            for pattern in patterns:
                matches = re.finditer(pattern, full_text)
                for match in matches:
                    speaker = match.group(1).strip()
                    content = match.group(2).strip()
                    if speaker and content:
                        speeches.append((speaker, content))
            
            # 중복 제거
            speeches = list(set(speeches))
            
            self.stdout.write(f"발언 패턴 {len(speeches)}개 발견")
            
            # 발견된 첫 발언 샘플 출력
            if speeches:
                self.stdout.write("\n발언 샘플:")
                speaker, content = speeches[0]
                self.stdout.write(f"\n발언자: {speaker}")
                self.stdout.write(f"내용: {content[:100]}...")
                self.stdout.write("\n" + "="*50 + "\n")
            
            return speeches
            
        except Exception as e:
            raise Exception(f'발언 추출 중 오류: {str(e)}')

    def wait_for_download(self, download_path, timeout=60):  # 시간 늘림
        """완전한 PDF 파일이 다운로드될 때까지 대기"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            files = os.listdir(download_path)
            pdf_files = [f for f in files if f.endswith('.PDF') or f.endswith('.pdf')]
            
            if pdf_files:
                # PDF 파일이 있고 크기가 변하지 않을 때까지 대기
                pdf_path = os.path.join(download_path, pdf_files[0])
                initial_size = os.path.getsize(pdf_path)
                time.sleep(2)  # 2초 대기
                if os.path.getsize(pdf_path) == initial_size:  # 크기가 같으면 다운로드 완료
                    return pdf_files[0]
            
            self.stdout.write("다운로드 대기 중...")
            time.sleep(2)
        return None

    def handle(self, *args, **options):
        # Chrome 설정
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        
        # 다운로드 경로 설정
        download_path = os.path.join(os.getcwd(), 'temp_downloads')
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        else:
            # 기존 다운로드 폴더 정리
            for file in os.listdir(download_path):
                try:
                    os.remove(os.path.join(download_path, file))
                except:
                    pass
        
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': download_path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'plugins.always_open_pdf_externally': True
        })
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # 처 번째 회의록만 선택
            conferences = Conference.objects.filter(conferencecontent__isnull=True)[:1]
            self.stdout.write(f"첫 번째 회의록을 처리합니다...")
            
            success_count = 0
            error_count = 0
            
            for conf in tqdm(conferences):
                try:
                    self.stdout.write(f"\n회의록 처리 시작: {conf.회의록ID}")
                    
                    # 다운로드 폴더 비우기
                    for file in os.listdir(download_path):
                        try:
                            os.remove(os.path.join(download_path, file))
                        except:
                            pass
                    
                    driver.get(conf.회의록URL)
                    
                    # 완전한 PDF 파일 대기
                    pdf_filename = self.wait_for_download(download_path)
                    
                    if pdf_filename:
                        pdf_path = os.path.join(download_path, pdf_filename)
                        file_size = os.path.getsize(pdf_path)
                        self.stdout.write(f"다운로드된 파일: {pdf_filename} ({file_size} bytes)")
                        
                        if file_size > 1000:
                            # 파일이 실제로 존재하는지 한 번 더 확인
                            if os.path.exists(pdf_path):
                                # PDF에서 발언 추출
                                speeches = self.extract_speeches(pdf_path)
                                
                                # 발언 저장
                                speech_count = 0
                                for speaker, content in speeches:
                                    name_match = re.search(r'([가-힣]+)', speaker)
                                    if name_match:
                                        speaker_name = name_match.group(1)
                                        self.stdout.write(f"발언자 발견: {speaker_name}")
                                        
                                        try:
                                            member = AssemblyMember.objects.get(이름__contains=speaker_name)
                                            
                                            SpeechRecord.objects.create(
                                                conference=conf,
                                                assembly_member=member,
                                                content=content,
                                                speech_order=speech_count + 1
                                            )
                                            speech_count += 1
                                            
                                        except AssemblyMember.DoesNotExist:
                                            self.stdout.write(f"미등록 발언자: {speaker_name}")
                                        except AssemblyMember.MultipleObjectsReturned:
                                            self.stdout.write(f"중복된 발언자: {speaker_name}")
                                
                                self.stdout.write(f"발언 {speech_count}개 저장 완료")
                                success_count += 1
                            else:
                                raise Exception("PDF 파일이 존재하지 않습니다")
                        else:
                            self.stdout.write(self.style.WARNING(f'의심스러운 파일 크기: {file_size} bytes'))
                            error_count += 1
                    else:
                        raise Exception("PDF 다운로드 시간 초과")
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'회의록 처리 중 오류 발생 ({conf.회의록ID}): {str(e)}'))
                    error_count += 1
                    continue
                
                # 다운로드 폴더 정리
                for file in os.listdir(download_path):
                    try:
                        os.remove(os.path.join(download_path, file))
                    except:
                        pass
                
        finally:
            driver.quit()
            if os.path.exists(download_path):
                for file in os.listdir(download_path):
                    try:
                        os.remove(os.path.join(download_path, file))
                    except:
                        pass
                os.rmdir(download_path)
            
        self.stdout.write(self.style.SUCCESS(f'\n처리 완료:'))
        self.stdout.write(f'성공: {success_count}개')
        self.stdout.write(f'실패: {error_count}개') 