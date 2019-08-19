from rest_framework import serializers

from api.fields import (
        AbsoluteURLField,
        LikeField,
    )

from apps.account.models import (
        Profile,
        Writer,
    )


class ProfileListSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    image = AbsoluteURLField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'name',
            'image',
        ]


class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    image = AbsoluteURLField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'email',
            'name',
            'image',
            'phone_num',
        ]


class CreateOrUpdateProfileSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = [
            'email',
            'username',
            'password',
            'name',
            'image',
            'phone_num',
        ]

    def to_representation(self, instance):
        return ProfileSerializer(instance).data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        password = self.validated_data.pop('password', None)
        user = instance.user
        user.username = self.validated_data.pop('username', user.username)
        user.email = self.validated_data.pop('email', user.email)
        if password is not None:
            user.set_password(password)
        user.save()
        return instance


class WriterListSerializer(serializers.ModelSerializer):

    image = AbsoluteURLField()
    like = LikeField()

    class Meta:
        model = Writer
        fields = [
            'id',
            'name',
            'image',
            'like',
        ]


class WriterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    image = AbsoluteURLField()
    like = LikeField()

    class Meta:
        model = Writer
        fields = [
            'id',
            'username',
            'email',
            'name',
            'introduction',
            'image',
            'phone_num',
            'instagram',
            'facebook',
            'like',
        ]


class CreateOrUpdateWriterSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = [
            'username',
            'password',
            'email',
            'name',
            'introduction',
            'image',
            'phone_num',
            'instagram',
            'facebook',
        ]

    def to_representation(self, instance):
        return WriterSerializer(instance).data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        password = self.validated_data.pop('password', None)
        user = instance.user
        user.username = self.validated_data.pop('username', user.username)
        user.email = self.validated_data.pop('email', user.email)
        if password is not None:
            user.set_password(password)
        user.save()
        return instance
