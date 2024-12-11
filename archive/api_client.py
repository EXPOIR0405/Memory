import os
import requests
from datetime import datetime

class AssemblyAPI:
    def __init__(self):
        self.api_url = "https://open.assembly.go.kr/portal/openapi/ALLNAMEMBER"
        self.params = {
            'KEY': os.getenv('ASSEMBLY_API_KEY', 'sample'),
            'Type': 'json',
            'pIndex': 1,
            'pSize': 100
        }

    def get_assembly_members(self):
        try:
            all_members = []
            page = 1
            
            while True:
                self.params['pIndex'] = page
                print(f"\n요청 URL과 파라미터: {self.api_url}")
                print(f"파라미터: {self.params}")
                
                response = requests.get(self.api_url, params=self.params)
                print(f"응답 상태 코드: {response.status_code}")
                
                data = response.json()
                
                if 'ALLNAMEMBER' in data and len(data['ALLNAMEMBER']) > 1:
                    items = data['ALLNAMEMBER'][1].get('row', [])
                    print(f"현재 페이지 데이터 수: {len(items)}")
                    
                    if not items:
                        print("더 이상 데이터가 없습니다.")
                        break
                        
                    for member in items:
                        # GTELT_ERACO 값이 문자열인지 확인하고 22대 의원만 필터링
                        daesu = member.get('GTELT_ERACO', '')
                        if isinstance(daesu, str) and '제22대' in daesu:
                            processed_member = {
                                'id': member.get('NAAS_CD', ''),
                                '이름': member.get('NAAS_NM', ''),
                                '한자이름': member.get('NAAS_CH_NM', ''),
                                '영문이름': member.get('NAAS_EN_NM', ''),
                                '생년월일': member.get('BIRDY_DT', ''),
                                '직책': member.get('DTY_NM', ''),
                                '정당': member.get('PLPT_NM', '').split('/')[0] if member.get('PLPT_NM') else '',
                                '선거구': member.get('ELECD_NM', '').split('/')[0] if member.get('ELECD_NM') else '',
                                '선거구구분': member.get('ELECD_DIV_NM', ''),
                                '위원회': member.get('CMIT_NM', ''),
                                '소속위원회': member.get('BLNG_CMIT_NM', ''),
                                '당선횟수': member.get('RLCT_DIV_NM', ''),
                                '당선대수': member.get('GTELT_ERACO', ''),
                                '성별': member.get('NTR_DIV', ''),
                                '전화번호': member.get('NAAS_TEL_NO', ''),
                                '이메일': member.get('NAAS_EMAIL_ADDR', ''),
                                '홈페이지': member.get('NAAS_HP_URL', ''),
                                '보좌관': member.get('AIDE_NM', ''),
                                '비서관': member.get('CHF_SCRT_NM', ''),
                                '비서': member.get('SCRT_NM', ''),
                                '약력': member.get('BRF_HST', ''),
                                '사무실호실': member.get('OFFM_RNUM_NO', ''),
                                '사진': member.get('NAAS_PIC', '')
                            }
                            all_members.append(processed_member)
                    
                    page += 1
                else:
                    print("응답 데이터 구조가 올바르지 않습니다.")
                    break
                    
            print(f"총 처리된 의원 수: {len(all_members)}")
            return all_members

        except Exception as e:
            print(f"API 호출 중 오류 발생: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []