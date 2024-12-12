from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Politician, Statement, Tag, KeywordAlert, MemberAlert
from .serializers import PoliticianSerializer, StatementSerializer, TagSerializer
from .services.analysis_service import ConferenceAnalyzer

class PoliticianViewSet(viewsets.ModelViewSet):
    queryset = Politician.objects.all()
    serializer_class = PoliticianSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'party', 'position']
    ordering_fields = ['name', 'created_at']

class StatementViewSet(viewsets.ModelViewSet):
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'source', 'politician__name']
    ordering_fields = ['statement_date', 'created_at']

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class AnalysisViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzer = ConferenceAnalyzer()

    @action(detail=False, methods=['get'])
    def keyword_search(self, request):
        keyword = request.query_params.get('keyword')
        results = self.analyzer.search_keyword(keyword)
        return Response(results)

    @action(detail=False, methods=['get'])
    def member_stats(self, request):
        stats = self.analyzer.get_member_speech_stats()
        return Response(stats)

    @action(detail=False, methods=['get'])
    def committee_topics(self, request):
        committee = request.query_params.get('committee')
        topics = self.analyzer.analyze_committee_topics(committee)
        return Response(topics)

class AlertViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def create_keyword_alert(self, request):
        keyword = request.data.get('keyword')
        KeywordAlert.objects.create(
            user=request.user,
            keyword=keyword
        )
        return Response({'status': 'success'})

    @action(detail=False, methods=['post'])
    def create_member_alert(self, request):
        member_id = request.data.get('member_id')
        MemberAlert.objects.create(
            user=request.user,
            assembly_member_id=member_id
        )
        return Response({'status': 'success'})
