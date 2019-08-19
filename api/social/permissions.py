from rest_framework import permissions

from apps.social.models import Comment


class CommentPermission(permissions.BasePermission):

    UNSAFE_ACTIONS = ['PATCH', 'PUT', 'DELETE', ]

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        if request.method.upper() in self.UNSAFE_ACTIONS:
            comment = Comment.objects.get(id=request.resolver_match.kwargs.get('pk'))
            if comment.profile.user == request.user:
                return True
        return False
