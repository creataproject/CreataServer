from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from apps.account.models import (
        Profile,
        Writer,
    )
from apps.post.admin import PostInline


class UserAdmin(BaseUserAdmin):

    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        UserAdmin.list_display = ['id', 'view_name', 'username', 'date_joined', 'is_active', ]
    ordering = ['-date_joined',]

    def view_name(self, obj):
        return '{}'.format(Profile.objects.get(user=obj).name)
    view_name.short_description = '이름'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ['id', 'view_user', 'name', 'view_image', 'view_email', 'phone_num', 'view_is_active', 'view_date_joined', ]
    ordering = ['-name', ]
    readonly_fields = ['view_user', 'view_image', 'view_email', 'view_is_active', 'view_date_joined', ]
    search_fields = ['name', ]
    fieldsets = [
        ('개인정보', {'fields': [
            'view_user',
            'name',
            'image',
            'phone_num',
        ]}),
    ]
    actions = ['do_deactive', 'do_active', ]

    def view_user(self, obj):
        return format_html('<a href="/auth/user/{id}/change">{name}</a>'.format(id=str(obj.user.id), name=obj.user.username))
    view_user.short_description = '사용자'

    def view_image(self, obj):
        if obj.image != '':
            link = str(obj.image)
            if 'http' not in link:
                link = obj.image.url
            return format_html('<img src="{link}" height="50px"/>'.format(link=link))
        return '-'
    view_image.short_description = '이미지'

    def view_email(self, obj):
        return obj.user.email
    view_email.short_description = '이메일'

    def view_is_active(self, obj):
        if obj.user.is_active:
            return format_html('<span style="color:green;">활동중</span>')
        return format_html('<span style="color:red;">탈퇴</span>')
    view_is_active.short_description = '활동 여부'

    def view_date_joined(self, obj):
        return obj.user.date_joined
    view_date_joined.short_description = '가입 시간'

    def do_deactive(self, request, queryset):
        User.objects.filter(id__in=queryset.values_list('user__id', flat=True)).update(is_active=False)
    do_deactive.short_description = '선택된 사용자를 비활성화합니다.'

    def do_active(self, request, queryset):
        User.objects.filter(id__in=queryset.values_list('user__id', flat=True)).update(is_active=True)
    do_active.short_description = '선택된 사용자를 활성화합니다.'


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):

    list_display = ['id', 'view_user', 'name', 'view_image', 'view_email', 'phone_num', 'view_is_active', 'view_date_joined', ]
    ordering = ['-name', ]
    readonly_fields = ['view_user', 'view_image', 'view_email', 'view_is_active', 'view_date_joined', ]
    search_fields = ['name', ]
    inlines = [PostInline, ]
    fieldsets = [
        ('개인정보', {'fields': [
            'user',
            'name',
            'introduction',
            'image',
            'phone_num',
        ]}),
        ('SNS', {'fields': [
            'instagram',
            'facebook',
        ]}),
    ]
    actions = ['do_deactive', 'do_active', ]

    def view_user(self, obj):
        return format_html('<a href="/auth/user/{id}/change">{name}</a>'.format(id=str(obj.user.id), name=obj.user.username))
    view_user.short_description = '사용자'

    def view_image(self, obj):
        if obj.image != '':
            link = str(obj.image)
            if 'http' not in link:
                link = obj.image.url
            return format_html('<img src="{link}" height="50px"/>'.format(link=link))
        return '-'
    view_image.short_description = '이미지'

    def view_email(self, obj):
        return obj.user.email
    view_email.short_description = '이메일'

    def view_is_active(self, obj):
        if obj.user.is_active:
            return format_html('<span style="color:green;">활동중</span>')
        return format_html('<span style="color:red;">탈퇴</span>')
    view_is_active.short_description = '활동 여부'

    def view_date_joined(self, obj):
        return obj.user.date_joined
    view_date_joined.short_description = '가입 시간'

    def do_deactive(self, request, queryset):
        User.objects.filter(id__in=queryset.values_list('user__id', flat=True)).update(is_active=False)
    do_deactive.short_description = '선택된 사용자를 비활성화합니다.'

    def do_active(self, request, queryset):
        User.objects.filter(id__in=queryset.values_list('user__id', flat=True)).update(is_active=True)
    do_active.short_description = '선택된 사용자를 활성화합니다.'