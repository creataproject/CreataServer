from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.account.viewsets import (
        ProfileViewSet,
        WriterViewSet,
    )
from api.post.viewsets import (
        PostViewSet,
        TagViewSet,
    )
from api.social.viewsets import (
        CommentViewSet,
        LikeViewSet,
    )

app_name = 'api'

router = DefaultRouter()

router.register('profile', ProfileViewSet)
router.register('writer', WriterViewSet)
router.register('post', PostViewSet)
router.register('tag', TagViewSet)
router.register('like', LikeViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]