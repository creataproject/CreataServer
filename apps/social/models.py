from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from apps.account.models import Profile


class Like(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='프로필')
    is_liked = models.BooleanField('좋아요 여부', default=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'
        ordering = ['profile', ]

    def __str__(self):
        return '{name}님이 좋아요를 {like}(했)습니다.'.format(name=self.profile.name, like='눌렀' if self.is_liked else '취소')


class Comment(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='작성자')
    content = models.TextField('내용')
    created_at = models.DateTimeField('생성 날짜', auto_now_add=True)
    edited_at = models.DateTimeField('수정 날짜', auto_now=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    blocked_message = models.TextField('차단 메시지', default='관리자의 권한으로 삭제된 메세지입니다.', help_text='차단 여부가 활성화되면 해당 메시지가 보여집니다.')
    is_blocked = models.BooleanField('차단 여부', default=False)

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
        ordering = ['-created_at', ]

    def __str__(self):
        return '{id} : {name}님의 댓글 "{content}..."'.format(id=self.id, name=self.profile.name, content=self.content[:20])

    def get_content(self):
        if self.is_blocked:
            return self.blocked_message
        return self.content



