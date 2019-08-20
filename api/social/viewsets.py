from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.account.models import Profile
from apps.constants import ContentTypes
from apps.social.models import (
        Comment,
        Like,
    )

from api.social.serializers import (
        CommentSerializer,
        LikeSerializer,
    )
from api.social.pagination import CommentPagination
from api.social.permissions import CommentPermission
from api.logging import LoggingMixin


class LikeViewSet(LoggingMixin, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Like.objects.filter(is_liked=True)
    serializer_class = LikeSerializer
    serializer_classes = {
        'partial_update': LikeSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    @action(detail=False, methods=['PATCH', ], url_path='object/(?P<object>[a-z]+)/id/(?P<id>[0-9]+)')
    def click(self, request, object, id):

        if object is None or id is None:
            return Response(404, dict(message='필수 값이 입력되지 않았습니다.'))

        profile = Profile.objects.get(user=request.user)
        _, _ = Like.objects.get_or_create(
                                    content_type=ContentTypes.string_to_contenttype(object),
                                    object_id=id,
                                    profile=profile,
                                )
        return Response()


class CommentViewSet(LoggingMixin, viewsets.ModelViewSet):

    permission_classes = [CommentPermission, ]
    pagination_class = CommentPagination
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    serializer_classes = {
        'list': CommentSerializer,
        'retrieve': CommentSerializer,
        'create': CommentSerializer,
        'partial_update': CommentSerializer,
        'delete': CommentSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        # @Todo 순서
        # 1. like 많은 3개의 댓글
        # 2. 날짜가 최신인 댓글

        object = request.GET.get('object', None)
        id = request.GET.get('id', None)
        comment_qs = Comment.objects.filter(content_type__model=object, object_id=id)
        page = self.paginate_queryset(comment_qs)
        if page is not None:
            queryset = page
        serializer = self.get_serializer(queryset, context=self.get_serializer_context(), many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):

        object = request.GET.get('object', None)
        id = request.GET.get('id', None)
        content = request.data.get('content', None)

        if object is None or id is None:
            return Response(status=404, data=dict(message='필수 값이 입력되지 않았습니다.'))

        profile = Profile.objects.get(user=request.user)
        comment = Comment.objects.create(
                                    content_type=ContentTypes.string_to_contenttype(object),
                                    object_id=id,
                                    profile=profile,
                                    content=content,
                                )
        return Response(CommentSerializer(comment, context=self.get_serializer_context()).data)

    def partial_update(self, request, pk):
        content = request.data.get('content', None)
        Comment.objects.filter(id=pk).update(content=content)
        return Response()