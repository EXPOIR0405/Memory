from django.contrib import admin
from django.utils.html import format_html
from .models import AssemblyMember, Conference, ConferenceContent, SpeechRecord

class SpeechInline(admin.TabularInline):
    model = SpeechRecord
    extra = 0
    fields = ['assembly_member', 'speech_order', 'content']
    raw_id_fields = ['assembly_member']

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['회의록ID', '대수', '회기', '차수', '회의일자', '회의종류', '위원회명', 'speech_count']
    list_filter = ['대수', '회의종류', '위원회명', '회의일자']
    search_fields = ['회의록ID', '위원회명']
    ordering = ['-회의일자']
    inlines = [SpeechInline]
    
    def speech_count(self, obj):
        return obj.speechrecord_set.count()
    speech_count.short_description = '발언 수'

@admin.register(AssemblyMember)
class AssemblyMemberAdmin(admin.ModelAdmin):
    list_display = ['이름', '정당', '선거구', '당선횟수', 'photo_display', 'speech_count']
    list_filter = ['정당', '당선횟수']
    search_fields = ['이름', '정당', '선거구']
    ordering = ['이름']
    
    def photo_display(self, obj):
        if obj.사진:
            return format_html('<img src="{}" width="50" height="70" />', obj.사진)
        return "No photo"
    photo_display.short_description = '사진'
    
    def speech_count(self, obj):
        return obj.speechrecord_set.count()
    speech_count.short_description = '발언 수'

@admin.register(SpeechRecord)
class SpeechRecordAdmin(admin.ModelAdmin):
    list_display = ['conference', 'assembly_member', 'speech_order', 'short_content']
    list_filter = ['conference__회의종류', 'conference__위원회명', 'assembly_member__정당']
    search_fields = ['content', 'assembly_member__이름']
    raw_id_fields = ['conference', 'assembly_member']
    
    def short_content(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    short_content.short_description = '발언내용'

# 기존 ConferenceContent Admin 설정
@admin.register(ConferenceContent)
class ConferenceContentAdmin(admin.ModelAdmin):
    list_display = ['conference', 'parsed_at']
    search_fields = ['conference__회의록ID']
