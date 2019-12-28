from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from member.serializers import UserSerializer
from .models import Dream, Result


class DreamSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_completed = SerializerMethodField()

    class Meta:
        model = Dream
        fields = (
            'user',
            'id',
            'title',
            'description',
            'start_at',
            'complete_by',
            'tag',
            'created_at',
            'updated_at',
            'is_completed'
        )
        read_only_fields = ('created_at', 'updated_at', )

    def get_is_completed(self, obj):
        try:
            if obj.result:
                return True
        except ObjectDoesNotExist:
            return False


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = (
            'complete_at',
            'review',
            'photo',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at', )

