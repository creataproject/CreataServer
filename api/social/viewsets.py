from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.account.models import Profile
from apps.constants import ContentTypes
from apps.social.models import (
        Comment,
        Like,
    )

from api.social.serializers import CommentSerializer
from api.social.pagination import CommentPagination
from api.social.permissions import CommentPermission
from api.logging import LoggingMixin


class LikeViewSet(LoggingMixin, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Like.objects.filter(is_liked=True)

    def partial_update(self, request, *args, **kwargs):
        object = request.GET.get('object', None)
        id = request.GET.get('id', None)

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
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        # 1. like 많은 3개의 댓글
        # 2. 날짜가 최신인 댓글
        pass

    def partial_update(self, request, *args, **kwargs):
        object = request.GET.get('object', None)
        id = request.GET.get('id', None)

        if object is None or id is None:
            return Response(404, dict(message='필수 값이 입력되지 않았습니다.'))

        profile = Profile.objects.get(user=request.user)
        comment, _ = Comment.objects.get_or_create(
                content_type=ContentTypes.string_to_contenttype(object),
                object_id=id,
                profile=profile,
            )
        return Response(CommentSerializer(comment).data)