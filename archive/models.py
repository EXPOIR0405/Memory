from django.db import models

class AssemblyMember(models.Model):
    의원코드 = models.CharField(max_length=20, unique=True, null=True, blank=True)
    이름 = models.CharField(max_length=100, null=True, blank=True)
    한자이름 = models.CharField(max_length=100, blank=True, null=True)
    영문이름 = models.CharField(max_length=200, blank=True, null=True)
    생년월일 = models.CharField(max_length=20, blank=True, null=True)
    직책 = models.CharField(max_length=200, blank=True, null=True)
    정당 = models.CharField(max_length=100, null=True, blank=True)
    선거구 = models.CharField(max_length=200, blank=True, null=True)
    선거구구분 = models.CharField(max_length=100, blank=True, null=True)
    위원회 = models.CharField(max_length=500, blank=True, null=True)
    소속위원회 = models.CharField(max_length=500, blank=True, null=True)
    당선횟수 = models.CharField(max_length=100, blank=True, null=True)
    당선대수 = models.CharField(max_length=100, blank=True, null=True)
    성별 = models.CharField(max_length=10, null=True, blank=True)
    전화번호 = models.CharField(max_length=100, blank=True, null=True)
    이메일 = models.CharField(max_length=200, blank=True, null=True)
    홈페이지 = models.URLField(max_length=500, blank=True, null=True)
    보좌관 = models.CharField(max_length=200, blank=True, null=True)
    비서관 = models.CharField(max_length=200, blank=True, null=True)
    비서 = models.CharField(max_length=200, blank=True, null=True)
    약력 = models.TextField(blank=True, null=True)
    사무실호실 = models.CharField(max_length=100, blank=True, null=True)
    사진 = models.URLField(max_length=500, blank=True, null=True)

    생성일시 = models.DateTimeField(auto_now_add=True)
    수정일시 = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.이름} ({self.정당})"