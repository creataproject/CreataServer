from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

from apps.utils import Util

import datetime


class EmailHistoryManager(models.Manager):

    def send(self, type, email):
        if type == EmailHistory.CODE:
            today = datetime.date.today()
            count = self.filter(
                            created_at__range=[datetime.datetime.combine(today, datetime.time.min), datetime.datetime.combine(today, datetime.time.max)],
                            email=email,
                            type=EmailHistory.CODE,
                        ).count()
            if count > 4:
                raise ValueError('5회 이상 인증코드를 전송하셨습니다.')

            email_list = list(email)

            code = Util.get_random_letter(6)
            content = '인증번호는 {} 입니다. 해당 인증번호를 정확하게 입력해주세요.'.format(str(code))

            message = loader.render_to_string(
                'code.html',
                {
                    'subject': '아이템 크롤링 오류',
                    'content': content,
                    'add_message': '',
                }
            )
            try:
                # @Todo 비동기
                send_mail('[닷다] 비밀번호 찾기 인증번호 입니다.', '', settings.DEFAULT_FROM_EMAIL, email_list, html_message=message)
                return self.create(email=email, content=content, type=type, code=code, is_success=True)
            except:
                return self.create(email=email, content=content, type=type, code=code, is_success=False)

    def check_code(self, code=None, email=None):
        sms_qs = self.filter(email=email, type=EmailHistory.CODE).order_by('-created_at').first()
        if sms_qs is None:
            return False
        if sms_qs.code != code:
            return False
        else:
            sms_qs.is_completed = True
            sms_qs.save()
            return True
        return False


class EmailHistory(models.Model):

    CODE = 1

    TYPE = (
        (CODE, '인증 코드'),
    )

    email = models.EmailField('이메일')
    content = models.TextField('내용')
    code = models.CharField('인증 코드', blank=True, null=True, max_length=7)
    type = models.PositiveSmallIntegerField('타입', choices=TYPE, default=CODE)
    created_at = models.DateTimeField('생성 날짜', auto_now=True)
    is_success = models.BooleanField('성공 여부', default=False)
    is_completed = models.BooleanField('인증 완료 여부', default=False)

    objects = EmailHistoryManager()

    class Meta:
        verbose_name = 'Email 내역'
        verbose_name_plural = 'Email 내역'
        ordering = ['-created_at', ]

    def __str__(self):
        return '{email} ({type})'.format(email=self.email, type=self.get_type_display())