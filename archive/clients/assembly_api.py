import requests
from typing import Dict, List

class AssemblyOpenAPI:
    BASE_URL = "https://open.assembly.go.kr/portal/openapi/VCONFAPIGCONFLIST"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_conference_list(self, era_code: str, committee_code: str = None, page: int = 1) -> List[Dict]:
        params = {
            'KEY': self.api_key,
            'Type': 'json',
            'pIndex': page,
            'pSize': 100,
            'ERACO': f'제{era_code}대'
        }
        
        if committee_code:
            params['CMIT_CD'] = committee_code
            
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        print(f"API 요청 URL: {response.url}")
        print(f"API 응답: {response.text[:1000]}")
        
        data = response.json()
        
        if 'VCONFAPIGCONFLIST' in data:
            result = data['VCONFAPIGCONFLIST']
            if isinstance(result, list) and len(result) > 1:
                return result[1].get('row', [])
        return []
    
    def get_all_conference_list(self, era_code: str, committee_code: str = None) -> List[Dict]:
        all_conferences = []
        page = 1
        
        while True:
            try:
                conferences = self.get_conference_list(era_code, committee_code, page)
                if not conferences:  # 더 이상 데이터가 없으면 종료
                    break
                    
                all_conferences.extend(conferences)
                page += 1
                
            except Exception as e:
                print(f"Error fetching page {page}: {str(e)}")  # logger 대신 print 사용
                break
                
        return all_conferences 