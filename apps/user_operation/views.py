from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserLeavingMessage
from .serializers import LeavingMessageSerializer


# Create your views here.

class LeavingMessageViewset(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言功能
    """
    # 用户验证
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)
