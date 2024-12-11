from django.contrib import admin
from .models import AssemblyMember

@admin.register(AssemblyMember)
class AssemblyMemberAdmin(admin.ModelAdmin):
    list_display = ['이름', '정당', '선거구', '당선횟수']
    list_filter = ['정당', '당선횟수']
    search_fields = ['이름', '정당', '선거구']
    ordering = ['이름']
