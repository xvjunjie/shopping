from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin
from .serializers import UserFavSerializer
from .models import UserFav

# User = get_user_model()


# Create your views here.
class UserFavViewset(CreateModelMixin,DestroyModelMixin,GenericViewSet):
    '''用户收藏'''
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer