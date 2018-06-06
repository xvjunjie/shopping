from django_filters.rest_framework import DjangoFilterBackend
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
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer