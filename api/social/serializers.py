from rest_framework import serializers

from api.account.serializers import ProfileListSerializer

from api.fields import LikeField

from apps.social.models import (
        Comment,
        Like,
    )


class CommentSerializer(serializers.ModelSerializer):

    profile = ProfileListSerializer()
    content = serializers.SerializerMethodField()
    like = LikeField(source='*')

    class Meta:
        model = Comment
        fields = [
            'id',
            'profile',
            'content',
            'created_at',
            'edited_at',
            'like',
        ]

    def get_content(self, obj):
        if obj.is_blocked:
            return obj.blocked_message
        return obj.content


class LikeSerializer(serializers.ModelSerializer):

    profile = ProfileListSerializer()
    content_type = serializers.CharField(source='content_type.model')

    class Meta:
        model = Like
        fields = [
            'profile',
            'is_liked',
            'content_type',
            'object_id',
        ]

