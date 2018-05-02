from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from goods.serializers import GoodsSerializer
from .models import Goods
from rest_framework.generics import ListAPIView
from goods.serializers import GoodsSerializer


class GoodsListView(ListAPIView):
    ''''''

    # APIView
    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     goods_serializer = GoodsSerializer(goods, many=True)
    #     return Response(goods_serializer.data)

    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer