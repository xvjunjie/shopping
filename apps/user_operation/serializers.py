# -*- coding:utf-8 -*-
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import UserLeavingMessage


class LeavingMessageSerializer(ModelSerializer):


    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")
