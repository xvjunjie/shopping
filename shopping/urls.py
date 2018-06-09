"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from shopping.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewset
from user_operation.views import UserFavViewset
from users.views import SmsCodeViewset,UserViewset
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
# 配置goods的url  
router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', CategoryViewset, base_name='categorys')
router.register(r'codes', SmsCodeViewset, base_name='codes')
router.register(r'users', UserViewset, base_name='users')
router.register(r'userfav', UserFavViewset, base_name='userfav')

urlpatterns = [
    url('xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    #     商品列表页 
    #     url(r'^goods/$', GoodsListView.as_view(), name='goods_list'),
    url(r'^', include(router.urls)),

    url(r'^docs/', include_docs_urls(title='title')),
    # 登陆的一个配置
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^jwt_token_auth/', obtain_jwt_token),
]
