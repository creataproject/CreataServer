from rest_framework import viewsets

from apps.post.models import (
        Post,
        Tag,
    )
from apps.post.filters import (
        PostFilter,
        TagFilter,
    )

from api.logging import LoggingMixin
from api.post.pagination import (
        PostPagination,
        TagPagination,
    )
from api.post.serializers import (
        PostListSerializer,
        PostSerializer,
        TagSerializer,
    )


class PostViewSet(LoggingMixin, viewsets.ModelViewSet):

    # permission_classes = [IsAuthenticated, ]
    pagination_class = PostPagination
    queryset = Post.objects.filter(is_public=True)
    serializer_class = PostSerializer
    serializer_classes = {
        'list': PostListSerializer,
        'retrieve': PostSerializer,
    }
    filterset_class = PostFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


class TagViewSet(LoggingMixin, viewsets.ModelViewSet):

    # permission_classes = [IsAuthenticated, ]
    pagination_class = TagPagination
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    serializer_classes = {
        'list': TagSerializer,
    }
    filterset_class = TagFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)