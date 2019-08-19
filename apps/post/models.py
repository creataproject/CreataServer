from django.db import models

from apps.account.models import Writer
from apps.utils import FilenameChanger


class Tag(models.Model):

    name = models.CharField('이름', max_length=127)

    class Meta:
        verbose_name = '태그'
        verbose_name_plural = '태그'
        ordering = ['-name', ]

    def __str__(self):
        return self.name


class Cut(models.Model):

    image = models.ImageField(upload_to=FilenameChanger('cut'), verbose_name='이미지')
    priority = models.PositiveSmallIntegerField('우선순위', default=1)
    created_at = models.DateTimeField('생성 날짜', auto_now_add=True)
    edited_at = models.DateTimeField('수정 날짜', auto_now=True)

    class Meta:
        verbose_name = '컷'
        verbose_name_plural = '컷'
        ordering = ['-created_at', ]


class Post(models.Model):

    writer = models.ForeignKey(Writer, null=True, on_delete=models.SET_NULL, verbose_name='작가')
    content = models.TextField('내용', blank=True, null=True, )
    tag = models.ManyToManyField(Tag, blank=True, null=True, verbose_name='태그')
    cut = models.ManyToManyField(Cut, verbose_name='컷')
    created_at = models.DateTimeField('생성 날짜', auto_now_add=True)
    edited_at = models.DateTimeField('수정 날짜', auto_now=True)
    is_public = models.BooleanField('공개 여부', default=False)

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = '포스트'
        ordering = ['-created_at', ]

    def __str__(self):
        return self.content


