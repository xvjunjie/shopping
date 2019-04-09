# -*- coding:utf-8 -*-
import datetime
import re
from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

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


validators = []


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(label='验证码', write_only=True, required=True, max_length=4, min_length=4,
                                 help_text='验证码',
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 })

    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,  # style名文密文设置
    )

    def validate_code(self, code):
        '''验证验证码'''
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by(
            "-add_time")  # initial 前端传过来的值

        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:  # 如果数据库中的code不等于传递进来的 code
                raise serializers.ValidationError("验证码错误")
        else:

            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')


class UserDetailSerializer(serializers.ModelSerializer):
    """
        用户详情序列化类
    """

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")
