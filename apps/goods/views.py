from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler

from .models import Goods, GoodsCategory, Banner
from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet






class GoodsListViewSet(ListModelMixin, RetrieveModelMixin,GenericViewSet):
    '''商品列表跟商品详情'''

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    filter_backends = (DjangoFilterBackend,SearchFilter, OrderingFilter)
    filter_fields = ('name', 'shop_price')
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')





class CategoryViewset(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    '''
    商品分类

    '''
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer

    # authentication_classes = (jw)


    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self): #user/id 获取用户
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()



class BannerViewset(ListModelMixin, GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer