from rest_framework import serializers

from apps.social.models import Like


class AbsoluteURLField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        try:
            return self.context['request'].build_absolute_uri(value.url)
        except:
            return None


class LikeField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        like_qs = Like.objects.filter(
                                content_type__model=value.__class__.__name__.lower(),
                                object_id=value.id,
                            )

        try:
            is_liked = like_qs.get(profile__user=self.context['request'].user).is_liked
        except:
            is_liked = False

        return dict(
                count=like_qs.filter(is_liked=True).count(),
                is_liked=is_liked,
            )