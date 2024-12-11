from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Politician, Statement, Tag
from .serializers import PoliticianSerializer, StatementSerializer, TagSerializer

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
