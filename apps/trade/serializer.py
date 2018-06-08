# -*- coding:utf-8 -*-
from rest_framework import serializers
from rest_framework.serializers import Serializer

from goods.models import Goods
from trade.models import ShoppingCart, OrderInfo


class ShopCartSerializer(Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())


    #加入购物车，判断购物车是否已经有该商品
    def create(self, validated_data):
        user = self.context["request"].user  #获取当前用户
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods) #是否存在

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # pay_status = serializers.CharField(read_only=True)
    # trade_no = serializers.CharField(read_only=True)
    # order_sn = serializers.CharField(read_only=True)
    # pay_time = serializers.DateTimeField(read_only=True)
    # alipay_url = serializers.SerializerMethodField(read_only=True)
    #
    # def get_alipay_url(self, obj):
    #     alipay = AliPay(
    #         appid="",
    #         app_notify_url="http://127.0.0.1:8000/alipay/return/",
    #         app_private_key_path=private_key_path,
    #         alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    #         debug=True,  # 默认False,
    #         return_url="http://127.0.0.1:8000/alipay/return/"
    #     )
    #
    #     url = alipay.direct_pay(
    #         subject=obj.order_sn,
    #         out_trade_no=obj.order_sn,
    #         total_amount=obj.order_mount,
    #     )
    #     re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    #
    #     return re_url
    #
    #
    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id, ranstr=random_ins.randint(10, 99))

        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"