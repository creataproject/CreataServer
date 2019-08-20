from django.contrib import admin
from django.utils.html import format_html

from apps.post.models import (
        Cut,
        Tag,
        Post,
    )
from apps.social.models import (
        Like,
        Comment,
    )
from apps.social.admin import (
        LikeInline,
        CommentInline,
    )

from apps.utils import Util


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', ]
    ordering = ['-name', ]


class CutInline(admin.TabularInline):

    model = Cut
    extra = 0
    readonly_fields = ['created_at', 'edited_at', ]

    def view_image(self, obj):
        try:
            return format_html('<img src="{link}" height="50px"/>'.format(link=obj.image.url))
        except:
            return '-'
    view_image.short_description = '이미지'


class PostInline(admin.StackedInline):

    model = Post
    extra = 0
    list_display = ['id', 'content', 'created_at', 'edited_at', 'is_public', ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'
    list_display = ['id', 'writer', 'title', 'created_at', 'edited_at', 'view_is_public', 'view_like_count', 'view_comment_count', ]
    list_filter = ['tags', ]
    search_fields = ['writer__name', 'tag__name', ]
    inlines = [CutInline, CommentInline, LikeInline, ]
    filter_horizontal = ['tags', ]
    readonly_fields = ['created_at', 'edited_at', ]
    fieldsets = [
        ('기본 정보', {'fields': [
            'writer',
            'title',
            'content',
            'tags',
        ]}),
        ('부가 정보', {'fields': [
            ('created_at', 'edited_at',),
            'is_public',
        ]}),
    ]
    actions = ['do_update_public', 'do_update_private', ]

    def view_like_count(self, obj):
        return str(Like.objects.filter(
                                    content_type__model='post',
                                    object_id=obj.id,
                                    is_liked=True).count()) + '개'
    view_like_count.short_description = '좋아요'

    def view_comment_count(self, obj):
        return str(Comment.objects.filter(
                                    content_type__model='post',
                                    object_id=obj.id).count()) + '개'
    view_comment_count.short_description = '댓글'

    def view_is_public(self, obj):
        if obj.is_public:
            return format_html('<span style="color:green;">공개</span>')
        return format_html('<span style="color:red;">비공개</span>')
    view_is_public.short_description = '공개 여부'

    def get_review(self, obj):
        return Util.add_unit(Comment.objects.filter(content_type__model='post', object_id=obj.id).count()) + '개'
    get_review.short_description = '댓글'

    def get_like(self, obj):
        return Util.add_unit(Like.objects.filter(
                                                content_type__model='post',
                                                object_id=obj.id,
                                                is_liked=True,
                                            ).count()) + '개'
    get_like.short_description = '좋아요'

    def do_update_public(self, request, queryset):
        queryset.update(is_public=True)
    do_update_public.short_description = '선택된 리뷰를 공개로 전환합니다.'

    def do_update_private(self, request, queryset):
        queryset.update(is_public=False)
    do_update_private.short_description = '선택된 아이템을 비공개로 전환합니다.'