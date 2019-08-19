from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apps.utils import FilenameChanger


class UserAdmin(BaseUserAdmin):

    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        UserAdmin.list_display = ['id', 'view_nickname', 'view_name', 'username', 'date_joined', 'is_active', ]
    ordering = ['-date_joined',]

    def view_nickname(self, obj):
        return '{}'.format(Profile.objects.get(user=obj).nickname)
    view_nickname.short_description = '닉네임'

    def view_name(self, obj):
        return '{last_name}{first_name}'.format(last_name=obj.last_name, first_name=obj.first_name)
    view_name.short_description = '이름'

    def has_change_permission(self, request, obj=None):
        return False


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


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
        return '사용자 {}'.format(self.name)


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
        return '작가 {}'.format(self.name)