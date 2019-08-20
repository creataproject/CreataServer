from apps.account.models import (
        Profile,
        Writer,
    )
from apps.social.models import Like
import django_filters


class ProfileFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(label='이름', field_name='name', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['name', ]


class WriterFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(label='이름', field_name='name', lookup_expr='icontains')
    ordering = django_filters.CharFilter(label='순서', method='filter_ordering')
    like = django_filters.ModelChoiceFilter(label='좋아요', queryset=Profile.objects.all(), method='filter_like')

    class Meta:
        model = Writer
        fields = ['name', ]

    def filter_ordering(self, queryset, name, value):
        if value == 'recommend':
            pass
        return queryset

    def filter_like(self, queryset, name, value):
        post_id_list = list(Like.objects.filter(
                                            content_type__model='writer',
                                            profile=value,
                                            is_liked=True,)\
                                        .values_list('object_id', flat=True))
        return queryset.filter(id__in=post_id_list)
