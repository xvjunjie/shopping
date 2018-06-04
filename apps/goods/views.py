from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from goods import GoodsFilter
from .models import Goods
from goods.serializers import GoodsSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


# class GoodsListView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)




class GoodsListViewSet(ListModelMixin, GenericViewSet):
    ''''''

    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'shop_price')
    # filter_class = GoodsFilter
