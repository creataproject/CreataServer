from apps.account.models import (
        Profile,
        Writer,
    )
from apps.post.models import (
        Post,
        Tag,
    )
from apps.social.models import Like

import django_filters


class PostFilter(django_filters.FilterSet):

    writer = django_filters.CharFilter(label='작가', method='filter_writer')
    tag = django_filters.CharFilter(label='이름', method='filter_tag')
    like = django_filters.ModelChoiceFilter(label='좋아요', queryset=Profile.objects.all(), method='filter_like')

    class Meta:
        model = Post
        fields = ['writer', 'tag', ]

    def filter_writer(self, queryset, name, value):
        return queryset.filter(writer__name=value)

    def filter_tag(self, queryset, name, value):
        return queryset.filter(tag__name=value)

    def filter_like(self, queryset, name, value):
        post_id_list = list(Like.objects.filter(
                                            content_type__model='post',
                                            profile__id=value,
                                            is_liked=True,)\
                                        .values_list('object_id', flat=True))
        return queryset.filter(id__in=post_id_list)


class TagFilter(django_filters.FilterSet):

    writer = django_filters.ModelChoiceFilter(label='작가', queryset=Writer.objects.all(), method='filter_writer')
    name = django_filters.CharFilter(label='이름', field_name='name', lookup_expr='icontains')
    ordering = django_filters.CharFilter(label='순서', method='filter_ordering')

    class Meta:
        model = Tag
        fields = ['writer', 'name', 'ordering', ]

    def filter_ordering(self, queryset, name, value):
        if value == 'popular':
            pass
        return queryset

    def filter_writer(self, queryset, name, value):
        return queryset