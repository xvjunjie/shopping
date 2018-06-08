from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler

from .models import Goods,GoodsCategory
from goods.serializers import GoodsSerializer,CategorySerializer
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet



class GoodsListViewSet(ListModelMixin, GenericViewSet):
    '''商品列表'''

    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'shop_price')
    # filter_class = GoodsFilter




class CategoryViewset(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    '''
        list:
            列表
        retrieve:
            详情

    '''
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer

