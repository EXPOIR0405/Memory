from rest_framework import serializers
from .models import Politician, Statement, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class StatementSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Statement
        fields = ['id', 'content', 'source', 'statement_date', 'created_at', 'tags']

class PoliticianSerializer(serializers.ModelSerializer):
    statements = StatementSerializer(many=True, read_only=True)
    
    class Meta:
        model = Politician
        fields = ['id', 'name', 'party', 'position', 'created_at', 'statements'] 