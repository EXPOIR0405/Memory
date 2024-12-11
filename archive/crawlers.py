import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import Politician, Statement, Tag
import time
import re
import os

class NewsCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def parse_date(self, date_str):
        """날짜 문자열을 datetime 객체로 변환"""
        try:
            now = datetime.now()
            if '분 전' in date_str:
                minutes = int(date_str.replace('분 전', ''))
                return now.replace(minute=now.minute - minutes)
            elif '시간 전' in date_str:
                hours = int(date_str.replace('시간 전', ''))
                return now.replace(hour=now.hour - hours)
            elif '일 전' in date_str:
                days = int(date_str.replace('일 전', ''))
                return now.replace(day=now.day - days)
            else:
                return datetime.strptime(date_str, '%Y.%m.%d.')
        except Exception as e:
            return datetime.now()

    def crawl_news(self, politician_name, page=1):
        """
        뉴스 기사에서 정치인의 발언을 크롤링하는 메서드
        """
        try:
            # 페이지 정보를 포함한 URL 구성
            search_url = f"https://search.naver.com/search.naver?where=news&query={politician_name}&start={1 + (page-1)*10}"
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 여기에 실제 크롤링 로직 구현
            news_items = []
            articles = soup.select("div.news_wrap.api_ani_send")
            
            for article in articles:
                try:
                    # 제목과 본문 일부 추출
                    title = article.select_one("a.news_tit").text
                    content = article.select_one("a.api_txt_lines.dsc_txt_wrap").text
                    
                    # 언론사와 날짜 추출
                    press = article.select_one("a.info.press").text
                    date_str = article.select_one("span.info").text
                    
                    # 뉴스 링크 추출
                    news_link = article.select_one("a.news_tit")['href']
                    
                    # 날짜 변환
                    news_date = self.parse_date(date_str)
                    
                    news_items.append({
                        'content': f"[{title}] {content}",
                        'source': f"{press} ({news_link})",
                        'date': news_date,
                        'tags': ['뉴스']
                    })
                    
                except Exception as e:
                    print(f"기사 파싱 중 오류: {str(e)}")
                    continue
                
            return news_items
            
        except Exception as e:
            print(f"크롤링 중 오류 발생: {str(e)}")
            return []

    def save_statements(self, politician_name, statements):
        """크롤링한 발언을 데이터베이스에 저장"""
        try:
            politician = Politician.objects.get(name=politician_name)
            
            for statement_data in statements:
                # 중복 체크 (내용과 날짜로)
                existing = Statement.objects.filter(
                    politician=politician,
                    content=statement_data['content'],
                    statement_date=statement_data['date']
                ).exists()
                
                if not existing:
                    statement = Statement.objects.create(
                        politician=politician,
                        content=statement_data['content'],
                        source=statement_data['source'],
                        statement_date=statement_data['date']
                    )
                    
                    # 태그 처리
                    for tag_name in statement_data.get('tags', []):
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        statement.tags.add(tag)
                    
        except Politician.DoesNotExist:
            print(f"정치인을 찾을 수 없습니다: {politician_name}")
        except Exception as e:
            print(f"저장 중 오류 발생: {str(e)}") 

class AssemblyMemberCrawler:
    def __init__(self):
        self.api_key = os.getenv('ASSEMBLY_API_KEY')
        
    def crawl_members(self):
        """국회의원 정보 API 호출"""
        try:
            # 현재 국회의원 정보 조회 API
            url = "https://open.assembly.go.kr/portal/openapi/ALLNAMEMBER"
            params = {
                'Key': self.api_key,
                'Type': 'json',
                'pIndex': '1',
                'pSize': '300'  # 전체 의원 수 조회
            }
            
            print("API 요청 시작...")
            response = requests.get(url, params=params)
            print(f"API 응답 상태 코드: {response.status_code}")
            
            # 응답 내용 확인을 위한 디버깅
            print("API 응답 데이터:", response.text[:500])  # 처음 500자만 출력
            
            data = response.json()
            members = []
            
            # API 응답 구조 파악을 위한 출력
            print("\nAPI 응답 구조:")
            print(data.keys() if isinstance(data, dict) else "응답이 딕셔너리가 아님")
            
            # 실제 데이터 파싱 (API 응답 구조에 따라 수정 필요)
            if 'ALLNAMEMBER' in data:
                member_list = data['ALLNAMEMBER'][1]['row']
                for member in member_list:
                    members.append({
                        'name': member.get('HG_NM', ''),  # 한글 이름
                        'party': member.get('POLY_NM', ''),  # 소속정당
                        'position': '국회의원'
                    })
            
            print(f"\n총 {len(members)}명의 의원 정보를 가져왔습니다.")
            return members
            
        except Exception as e:
            print(f"API 호출 중 오류 발생: {str(e)}")
            return [] 