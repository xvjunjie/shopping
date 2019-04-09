# -*- coding:utf-8 -*-
from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer
from .models import UserFav
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import UserLeavingMessage, UserAddress


class UserFavSerializer(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        model = UserFav
        fields = ('user','goods')

class LeavingMessageSerializer(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")
