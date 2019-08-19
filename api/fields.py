from rest_framework import serializers

from apps.social.models import Like
from apps.post.models import Post


class AbsoluteURLField(serializers.Field):

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        try:
            return value.url
        except:
            return None


class LikeField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        model = value.__class__.__name__.lower()
        like_qs = Like.objects.filter(content_type__model=model, object_id=value.id)

        try:
            is_liked = like_qs.get(profile__user=self.context['request'].user).value('is_liked')
        except:
            is_liked = False

        return dict(
                count=like_qs.filter(is_liked=True).count(),
                is_liked=is_liked,
            )