# -*- coding:utf-8 -*-
from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer
from .models import UserFav

class UserFavSerializer(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )


    class Meta:
        model = UserFav
        fields = ('user','goods')