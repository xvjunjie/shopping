# -*- coding:utf-8 -*-
import datetime
import re
from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from shopping.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validated_moblie(self, mobile):
        '''
        验证手机号
        :param moblie:
        :return:
        '''

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile
