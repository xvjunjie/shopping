from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler

from .models import Goods,GoodsCategory
from goods.serializers import GoodsSerializer,CategorySerializer
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
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
    '''商品列表'''

    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'shop_price')
    # filter_class = GoodsFilter




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