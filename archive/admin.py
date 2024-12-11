from django.contrib import admin
from .models import Politician, Statement, Tag

@admin.register(Politician)
class PoliticianAdmin(admin.ModelAdmin):
    list_display = ['name', 'party', 'position', 'created_at']
    search_fields = ['name', 'party']
    list_filter = ['party', 'position']

@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ['politician', 'content', 'source', 'statement_date', 'created_at']
    search_fields = ['content', 'politician__name']
    list_filter = ['politician', 'statement_date']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
