from django.contrib import admin
from django.utils.html import format_html
from django.contrib.contenttypes.admin import (
        GenericTabularInline,
        GenericStackedInline,
    )

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


class CommentInline(GenericStackedInline):

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

    search_fields = ['profile__nickname', 'content', ]
    list_display = ['id', 'view_link', 'view_profile', 'content', 'is_blocked', 'created_at', 'edited_at', ]
    ordering = ['-created_at', ]
    inlines = [LikeInline, ]
    readonly_fields = ['id', 'profile', 'content', 'created_at', 'edited_at', 'content_type', 'object_id', ]
    actions = ['block_comment', ]

    def block_comment(self, request, queryset):
        queryset.update(is_blocked=True)
    block_comment.short_description = '관리자의 권한으로 댓글을 삭제합니다.'

    def view_profile(self, obj):
        link = '/account/profile/{id}/change/'.format(id=obj.profile.id)
        return format_html('<a href="{link}">{name}</a>'.format(link=link, name=obj.profile.nickname))
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

    search_fields = ['profile__nickname', ]
    list_display = ['id', 'view_link', 'view_profile', 'is_liked', ]
    ordering = ['profile', ]
    readonly_fields = ['id', 'profile', 'is_liked', 'content_type', 'object_id', ]

    def view_profile(self, obj):
        link = '/account/profile/{id}/change/'.format(id=obj.profile.id)
        return format_html('<a href="{link}">{name}</a>'.format(link=link, name=obj.profile.nickname))

    def view_link(self, obj):
        model = obj.content_type.model_class()
        link = '/{app}/{model}/{id}/change/'.format(
                                                    app=obj.content_type.app_label,
                                                    model=model.__name__.lower(),
                                                    id=obj.object_id
                                                )
        return format_html('<a href="{link}">{name}</a>'.format(link=link, name=model.objects.filter(id=obj.object_id).first().__str__()))