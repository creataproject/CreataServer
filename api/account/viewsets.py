from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.account.models import (
        Profile,
        Writer,
    )
from apps.account.filters import (
        WriterFilter,
        ProfileFilter,
    )
from apps.sender.models import EmailHistory

from api.account.pagination import (
        ProfilePagination,
        WriterPagination,
    )
from api.account.serializers import (
        ProfileListSerializer,
        ProfileSerializer,
        CreateOrUpdateProfileSerializer,
        WriterListSerializer,
        WriterSerializer,
        CreateOrUpdateWriterSerializer,
    )
from api.logging import LoggingMixin


class AuthenticationViewSet(LoggingMixin, viewsets.ModelViewSet):

    @action(detail=False, methods=['POST',], )
    def signup(self, request, *args, **kwargs):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user)

        serializer = CreateOrUpdateProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        token, created = Token.objects.get_or_create(user=user)
        data = dict(token=token.key, profile=serializer.data)

        if created:
            return Response(status=201, data=data)
        else:
            return Response(data=data)

    @action(detail=False, methods=['POST',], )
    def signin(self, request, *args, **kwargs):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user_qs = User.objects.filter(username=username, is_staff=False)
        if not user_qs.exists():
            return Response(status=400, data=dict(message='존재하지 않거나 올바르지 않은 아이디 입니다.'))
        user = authenticate(username=user_qs.first().username, password=password)
        if user is None:
            return Response(status=400, data=dict(message='올바르지 않은 비밀번호 입니다.'))
        token = Token.objects.get(user=user)
        profile = Profile.objects.get(user=user)
        return Response(dict(
            profile=ProfileSerializer(profile, context={'request': request}).data,
            token=token.key,
        ))

    @action(detail=False, methods=['POST', ], url_path='search/password')
    def search_password(self, request, *args, **kwargs):

        username = request.data.get('username', None)
        email = request.data.get('email', None)

        user = User.objects.filter(username=username, email=email)
        if user.exist():
            EmailHistory.object.send(type=EmailHistory.CODE, email=user.email)
            return Response(dict(message='해당 이메일로 인증 코드 전송을 완료하였습니다.'))
        return Response(dict(message='해당 이메일의 계정이 존재하지 않습니다.'))

    @action(detail=False, methods=['POST', ], url_path='verify/code')
    def verify_code(self, request, *args, **kwargs):

        email = request.data.get('email', None)
        code = request.data.get('code', None)

        if EmailHistory.objects.check_code(email=email, code=code):
            return Response(dict(message='인증이 완료되었습니다.'))
        return Response(400, dict(message='인증 번호가 올바르지 않습니다.'))

    @action(detail=False, methods=['POST', ], url_path='search/username')
    def search_username(self, request, *args, **kwargs):

        email = request.data.get('email', None)

        user = User.objects.filter(email=email)
        if user.exist():
            return Response(dict(username=user.username))
        return Response(dict(message='해당 이메일의 계정이 존재하지 않습니다.'))


class ProfileViewSet(LoggingMixin, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    pagination_class = ProfilePagination
    queryset = Profile.objects.filter(user__is_active=True)
    serializer_class = ProfileSerializer
    serializer_classes = {
        'list': ProfileListSerializer,
        'retrieve': ProfileSerializer,
        'create': CreateOrUpdateProfileSerializer,
    }
    filterset_class = ProfileFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)

        if request.method.upper() == 'GET':
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response(serializer.data)

        if request.method.upper() == 'PATCH':
            serializer = CreateOrUpdateProfileSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class WriterViewSet(LoggingMixin, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    pagination_class = WriterPagination
    queryset = Writer.objects.filter(user__is_active=True)
    serializer_class = WriterSerializer
    serializer_classes = {
        'list': WriterListSerializer,
        'retrieve': WriterSerializer,
        'create': CreateOrUpdateWriterSerializer,
    }

    filterset_class = WriterFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        writer = Writer.objects.get(user=request.user)

        if request.method.upper() == 'GET':
            serializer = WriterSerializer(writer, context={'request': request})
            return Response(serializer.data)

        if request.method.upper() == 'PATCH':
            serializer = CreateOrUpdateWriterSerializer(writer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
