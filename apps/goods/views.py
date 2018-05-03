from django_filters.rest_framework import DjangoFilterBackend

from goods import GoodsFilter
from .models import Goods
from goods.serializers import GoodsSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


class GoodsListViewSet(ListModelMixin, GenericViewSet):
    ''''''

    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'shop_price')
    # filter_class = GoodsFilter
