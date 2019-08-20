from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

from apps.social.models import (
        Like,
        Comment,
    )


class LikeInline(GenericTabularInline):

    model = Like
    extra = 0
    list_display = ['id', 'profile', 'is_liked', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


class ContentTypeFilter(SimpleListFilter):

    title = 'content_type'
    parameter_name = 'content_type'

    WRITER = '1'
    COMMENT = '2'
    POST = '3'

    def lookups(self, request, model_admin):
        return (
            (self.WRITER, '작가'),
            (self.COMMENT, '댓글'),
            (self.POST, '포스팅'),
        )

    def queryset(self, request, queryset):
        if self.value() == self.WRITER:
            return queryset.filter(content_type__model='writer')
        if self.value() == self.COMMENT:
            return queryset.filter(content_type__model='comment')
        if self.value() == self.POST:
            return queryset.filter(content_type__model='post')
        return queryset


class CommentInline(GenericTabularInline):

    model = Comment
    extra = 0
    list_display = ['id', 'profile', 'content', 'created_at', 'is_blocked', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    search_fields = ['profile__name', 'content', ]
    list_display = ['id', 'view_link', 'view_profile', 'content', 'created_at', 'edited_at', 'is_blocked', ]
    ordering = ['-created_at', ]
    inlines = [LikeInline, ]
    readonly_fields = ['id', 'profile', 'content', 'created_at', 'edited_at', 'content_type', 'object_id', ]
    fieldsets = [
        ('기본 정보', {'fields': [
            'profile',
            'content',
        ]}),
        ('차단 정보', {'fields': [
            'blocked_message',
            'is_blocked',
        ]}),
        ('부가 정보', {'fields': [
            ('created_at', 'edited_at',),
        ]}),
    ]
    actions = ['block_comment', ]

    def block_comment(self, request, queryset):
        queryset.update(is_blocked=True)
    block_comment.short_description = '관리자의 권한으로 댓글을 삭제합니다.'

    def view_profile(self, obj):
        link = '/account/profile/{id}/change/'.format(id=obj.profile.id)
        return format_html('<a href="{link}">{name}</a>'.format(link=link, name=obj.profile.name))
    view_profile.short_description = '사용자'

    def view_link(self, obj):
        model = obj.content_type.model_class()
        link = '/{app}/{model}/{id}/change/'.format(
                                                    app=obj.content_type.app_label,
                                                    model=model.__name__.lower(),
                                                    id=obj.object_id
                                                )
        return format_html('<a href="{link}">{name}</a>'.format(link=link, name=model.objects.filter(id=obj.object_id).first().__str__()))
    view_link.short_description = '링크'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    search_fields = ['profile__name', ]
    list_display = ['id', 'view_link', 'view_profile', 'is_liked', ]
    ordering = ['profile', ]
    list_filter = [ContentTypeFilter, ]
    readonly_fields = ['id', 'profile', 'is_liked', 'content_type', 'object_id', ]

    def view_profile(self, obj):

        link = '/account/profile/{id}/change/'.format(id=obj.profile.id)
        return format_html('<a href="{link}">{name}</a>'.format(link=link, name=obj.profile.name))

    def view_link(self, obj):

        model = obj.content_type.model_class()
        link = '/{app}/{model}/{id}/change/'.format(
                                                    app=obj.content_type.app_label,
                                                    model=model.__name__.lower(),
                                                    id=obj.object_id
                                                )
        return format_html('<a href="{link}">{name}</a>'.format(link=link, name=model.objects.filter(id=obj.object_id).first().__str__()))