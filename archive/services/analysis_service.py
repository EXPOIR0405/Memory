from collections import Counter
from django.db.models import Count
from archive.models import SpeechRecord, Conference, AssemblyMember

class ConferenceAnalyzer:
    def search_keyword(self, keyword, start_date=None, end_date=None):
        """키워드가 포함된 발언 검색"""
        query = SpeechRecord.objects.filter(content__icontains=keyword)
        if start_date:
            query = query.filter(conference__회의일자__gte=start_date)
        if end_date:
            query = query.filter(conference__회의일자__lte=end_date)
        return query

    def get_member_speech_stats(self, start_date=None, end_date=None):
        """정치인별 발언 횟수 분석"""
        query = SpeechRecord.objects.values(
            'assembly_member__이름', 
            'assembly_member__정당'
        ).annotate(
            speech_count=Count('id')
        ).order_by('-speech_count')
        
        if start_date:
            query = query.filter(conference__회의일자__gte=start_date)
        if end_date:
            query = query.filter(conference__회의일자__lte=end_date)
        
        return query

    def analyze_committee_topics(self, committee_name, limit=10):
        """위원회별 주요 키워드 분석"""
        speeches = SpeechRecord.objects.filter(
            conference__위원회명=committee_name
        ).values_list('content', flat=True)

        # 간단한 단어 빈도수 분석
        words = []
        for speech in speeches:
            # 공백으로 단어 분리 (간단한 방식)
            words.extend([word for word in speech.split() if len(word) > 1])

        # 키워드 빈도수 계산
        word_count = Counter(words)
        return word_count.most_common(limit) 