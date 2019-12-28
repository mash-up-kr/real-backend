from rest_framework import serializers
from django.contrib.auth import authenticate

from member.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'nickname',
            'email',
        )


class UserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'nickname',
            'email',
            'password',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "nickname")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"], validated_data["email"], validated_data["password"],
            nickname=validated_data["nickname"]
        )
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print(data)
        data['username'] = data['email']
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")