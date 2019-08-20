from django.db import models
from django.contrib.auth.models import User

from apps.utils import FilenameChanger


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='사용자')
    name = models.CharField('이름', max_length=15)
    image = models.ImageField(upload_to=FilenameChanger('profile/image'), blank=True, null=True, verbose_name='이미지')
    phone_num = models.CharField('전화번호', blank=True, null=True, unique=True, max_length=15, help_text='- 없이 숫자만 입력해주세요.')

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = '프로필'
        ordering = ['name', ]

    def __str__(self):
        return '{} (사용자)'.format(self.name)


class Writer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='사용자')
    name = models.CharField('이름', max_length=15)
    introduction = models.TextField('소개', blank=True, null=True, )
    image = models.ImageField(upload_to=FilenameChanger('writer/image'), blank=True, null=True, verbose_name='이미지')
    phone_num = models.CharField('전화번호', blank=True, null=True, unique=True, max_length=15)
    instagram = models.CharField('인스타그램', blank=True, null=True, max_length=1023)
    facebook = models.CharField('페이스북', blank=True, null=True, max_length=1023)

    class Meta:
        verbose_name = '작가'
        verbose_name_plural = '작가'
        ordering = ['name', ]

    def __str__(self):
        return '{} (작가)'.format(self.name)