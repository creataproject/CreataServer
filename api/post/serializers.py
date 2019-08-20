from rest_framework import serializers

from api.account.serializers import (
        WriterListSerializer,
        WriterSerializer,
    )
from api.fields import (
        AbsoluteURLField,
        LikeField,
    )

from apps.post.models import (
        Post,
        Tag,
        Cut,
    )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]


class CutSerializer(serializers.ModelSerializer):

    image = AbsoluteURLField()

    class Meta:
        model = Cut
        fields = [
            'id',
            'image',
            'priority',
        ]


class PostListSerializer(serializers.ModelSerializer):

    writer = WriterListSerializer()
    tags = TagSerializer(many=True)
    thumbnail = CutSerializer()
    like = LikeField(source='*')

    class Meta:
        model = Post
        fields = [
            'id',
            'writer',
            'title',
            'content',
            'tags',
            'thumbnail',
            'created_at',
            'edited_at',
            'is_public',
            'like',
        ]


class PostSerializer(serializers.ModelSerializer):

    writer = WriterSerializer()
    tags = TagSerializer(many=True)
    cuts = CutSerializer(many=True)
    like = LikeField(source='*')

    class Meta:
        model = Post
        fields = [
            'id',
            'writer',
            'title',
            'content',
            'tags',
            'cuts',
            'created_at',
            'edited_at',
            'is_public',
            'like',
        ]

