from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from random import choice

from django.contrib.auth import get_user_model
from rest_framework import status, authentication, permissions
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .models import VerifyCode
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer

from utils.yunpian import YunPian
from shopping.settings import APIKEY


User = get_user_model()

class CustomBackend(ModelBackend):
    '''
    自定义用户认证
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q (username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, GenericViewSet):
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = '1234567890'
        random_str = []

        for i in range(4):
            random_str.append(choice(seeds))

        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        yunpian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yunpian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:

            #保存
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)



class UserViewset(CreateModelMixin,RetrieveModelMixin,GenericViewSet):
    '''用户注册'''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()


 #用户认证
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer


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

