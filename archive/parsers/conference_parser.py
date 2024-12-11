import os
import requests
from tempfile import NamedTemporaryFile
import subprocess

class ConferenceParser:
    def __init__(self):
        self.temp_dir = 'temp_hwp'
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def download_hwp(self, url: str) -> str:
        """HWP 파일을 다운로드하고 임시 파일 경로를 반환합니다."""
        response = requests.get(url)
        response.raise_for_status()
        
        temp_file = NamedTemporaryFile(delete=False, suffix='.hwp', dir=self.temp_dir)
        temp_file.write(response.content)
        temp_file.close()
        
        return temp_file.name
    
    def parse_hwp(self, file_path: str) -> str:
        """HWP 파일을 텍스트로 변환합니다."""
        try:
            # hwp5txt 명령어를 사용하여 변환
            result = subprocess.run(['hwp5txt', file_path], 
                                 capture_output=True, 
                                 text=True, 
                                 encoding='utf-8')
            return result.stdout
        finally:
            # 임시 파일 삭제
            if os.path.exists(file_path):
                os.remove(file_path)
    
    def parse_conference(self, url: str) -> str:
        """회의록 URL에서 텍스트를 추출합니다."""
        hwp_path = self.download_hwp(url)
        return self.parse_hwp(hwp_path) 