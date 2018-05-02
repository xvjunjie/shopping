# -*- coding:utf-8 -*-
import json

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from django.core import serializers

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        '''
        通过django的view实现商品列表页 
        :param request:
        :return:
        '''

        json_list = []
        goods = Goods.objects.all()[:10]
        json_data = serializers.serialize('json',goods)
        json_data = json.loads(json_data)

        return JsonResponse(json_data,safe=False)

        # for good in goods:
        #
        #
        #
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)
        #
        # return HttpResponse(json.dumps(json_list), content_type='application/json')
