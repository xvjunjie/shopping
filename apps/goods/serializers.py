# -*- coding:utf-8 -*-
from rest_framework import serializers

from goods.models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    ''' Serializer'''
    # Serializer
    # name = serializers.CharField(required=True, max_length=100)
    # click_num = serializers.IntegerField(default=0)
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#
#     def create(self, validated_data):
#         pass