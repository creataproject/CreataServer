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


@admin.register(Cut)
class CutAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'
    list_display = ['id', 'view_image', 'priority', 'created_at', 'edited_at', ]
    readonly_fields = ['created_at', 'edited_at', ]
    fieldsets = [
        ('기본 정보', {'fields': [
            'image',
            'priority',
        ]}),
        ('부가 정보', {'fields': [
            ('created_at', 'edited_at',),
        ]}),
    ]

    def view_image(self, obj):
        if obj.image != '':
            link = str(obj.image)
            if 'http' not in link:
                link = obj.image.url
            return format_html('<img src="{link}" height="50px"/>'.format(link=link))
        return '-'
    view_image.short_description = '이미지'


class PostInline(admin.StackedInline):

    model = Post
    extra = 0
    list_display = ['id', 'content', 'created_at', 'edited_at', 'is_public', ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'
    list_display = ['id', 'writer', 'created_at', 'edited_at', 'view_is_public', ]
    search_fields = ['writer__name', 'tag__name', ]
    inlines = [CommentInline, LikeInline, ]
    filter_horizontal = ['cut', 'tag', ]
    readonly_fields = ['created_at', 'edited_at', ]
    fieldsets = [
        ('기본 정보', {'fields': [
            'writer',
            'content',
            'tag',
            'cut',
        ]}),
        ('부가 정보', {'fields': [
            ('created_at', 'edited_at',),
            'is_public',
        ]}),
    ]
    actions = ['do_update_public', 'do_update_private', ]

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