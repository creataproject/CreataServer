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
    tag = TagSerializer(many=True)
    cut = serializers.SerializerMethodField()
    like = LikeField()

    class Meta:
        model = Post
        fields = [
            'id',
            'writer',
            'title',
            'content',
            'tag',
            'cut',
            'created_at',
            'edited_at',
            'is_public',
            'like',
        ]

    def get_cut(self, obj):
        return CutSerializer(obj.cut.all().order_by('priority').first()).data


class PostSerializer(serializers.ModelSerializer):

    writer = WriterSerializer()
    tag = TagSerializer(many=True)
    cut = CutSerializer(many=True)
    like = LikeField()

    class Meta:
        model = Post
        fields = [
            'id',
            'writer',
            'title',
            'content',
            'tag',
            'cut',
            'created_at',
            'edited_at',
            'is_public',
            'like',
        ]

