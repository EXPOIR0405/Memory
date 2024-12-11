from django.contrib import admin
from .models import AssemblyMember, Conference, ConferenceContent

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['회의록ID', '대수', '회기', '차수', '회의일자', '회의종류', '위원회명']
    list_filter = ['대수', '회의종류', '위원회명']
    search_fields = ['회의록ID', '위원회명']
    ordering = ['-회의일자']

@admin.register(ConferenceContent)
class ConferenceContentAdmin(admin.ModelAdmin):
    list_display = ['conference', 'parsed_at']
    search_fields = ['conference__회의록ID']

@admin.register(AssemblyMember)
class AssemblyMemberAdmin(admin.ModelAdmin):
    list_display = ['이름', '정당', '선거구', '당선횟수']
    list_filter = ['정당', '당선횟수']
    search_fields = ['이름', '정당', '선거구']
    ordering = ['이름']
