from django.core.mail import send_mail
from django.conf import settings
from archive.models import KeywordAlert, MemberAlert, SpeechRecord

class AlertService:
    @staticmethod
    def check_keyword_alerts(speech_record):
        """새로운 발언에 대해 키워드 알림 체크"""
        alerts = KeywordAlert.objects.all()
        for alert in alerts:
            if alert.keyword in speech_record.content:
                print(f"키워드 '{alert.keyword}' 발견됨, 알림 발송 시도...")
                AlertService._send_keyword_alert(
                    alert.user,
                    alert.keyword,
                    speech_record
                )

    @staticmethod
    def check_member_alerts(speech_record):
        """새로운 발언에 대해 의원 알림 체크"""
        alerts = MemberAlert.objects.filter(
            assembly_member=speech_record.assembly_member
        )
        for alert in alerts:
            AlertService._send_member_alert(
                alert.user,
                speech_record
            )

    @staticmethod
    def _send_keyword_alert(user, keyword, speech_record):
        """키워드 알림 이메일 발송"""
        subject = f'키워드 알림: {keyword}'
        message = f"""
        설정하신 키워드 '{keyword}'가 포함된 새로운 발언이 등록되었습니다.
        
        회의: {speech_record.conference}
        발언자: {speech_record.assembly_member.이름}
        발언내용: {speech_record.content[:100]}...
        """
        
        try:
            print(f"이메일 발송 시도: {user.email}")
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            print("이메일 발송 성공!")
        except Exception as e:
            print(f"이메일 발송 실패: {str(e)}")

    @staticmethod
    def _send_member_alert(user, speech_record):
        """의원 발언 알림 이메일 발송"""
        subject = f'의원 발언 알림: {speech_record.assembly_member.이름}'
        message = f"""
        관심 의원의 새로운 발언이 등록되었습니다.
        
        의원: {speech_record.assembly_member.이름}
        회의: {speech_record.conference}
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        ) 