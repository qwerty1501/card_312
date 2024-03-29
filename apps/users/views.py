import uuid
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login

from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.users.models import User, BasicUser, Basket, Mycard, Bankcard, Subscr, Coment, Favorites, Likes
from apps.users.serializers import (UserSerializer, UserCRUDSerializer, CustomTokenRefreshSerializer,
                                    SendMessageSerializer, BasicUserRegisterSerializer, PartnerRegisterSerializer,
                                    SendMailSerializer)

from apps.utils.main import generateError, generateAuthInfo

from django.shortcuts import redirect
from django.views.generic.base import View


class MVSDynamicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'update':
            if request.user.is_authenticated:
                return True
            else:
                return False
        else:
            return True


class UserMVS(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [MVSDynamicPermission]
    lookup_field = 'uniqueId'
    serializer_class = UserSerializer

    def create(self, request):
        secretAdminKey = request.data.get('secretAdminKey')
        if secretAdminKey == settings.SECRET_ADMIN_KEY:
            serializer = UserCRUDSerializer(data={'password': settings.DEFAULT_PASSWORD}, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=f"{settings.CLIENT_URL}/user/{serializer.data['uniqueId']}")
        return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        unique_id = kwargs['uniqueId']
        user = User.objects.get(uniqueId=unique_id)
        serializer = UserCRUDSerializer(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordMVS(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCRUDSerializer;
    lookup_field = 'resetPasswordUUID';

    def create(self, request, *args, **kwargs):
        uniqueId = request.data.get('uniqueId');
        try:
            user = User.objects.get(uniqueId=uniqueId);
        except User.DoesNotExist:
            return Response(**generateError('USER_NOT_FOUND'));
        serializer = self.serializer_class(user, context={'request': request});
        data = serializer.data;
        if not data['email']:
            return Response(**generateError('EMAIL_NOT_SET'));
        try:
            uuidStr = uuid.uuid4();
            milliseconds_since_epoch = datetime.datetime.now().timestamp() * 1000;
            user.resetPasswordUUID = uuidStr;
            user.resetPasswordDate = int(milliseconds_since_epoch) + 3600000;
            user.save();
            html_message = f'<a href="{settings.CLIENT_URL}/reset-password/{uuidStr}">Click me</a>';
            send_mail(
                'Reset password',
                'Click this button to reset password',
                settings.EMAIL_HOST_USER,
                [data['email']],
                fail_silently=False,
                html_message=html_message
            );
            return Response();
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR);

    def retrieve(self, request, *args, **kwargs):
        resetPasswordUUID = kwargs[self.lookup_field];
        try:
            user = User.objects.get(resetPasswordUUID=resetPasswordUUID);
        except User.DoesNotExist:
            return Response(**generateError('NOT_FOUND'));
        serializer = self.serializer_class(user, context={'request': request});
        milliseconds_since_epoch = datetime.datetime.now().timestamp() * 1000;
        if int(milliseconds_since_epoch) > serializer.data['resetPasswordDate']:
            return Response(**generateError('EXPIRED'));
        return Response(status=status.HTTP_200_OK);

    def update(self, request, *args, **kwargs):
        resetPasswordUUID = kwargs[self.lookup_field];
        password = request.data.get('password');
        try:
            user = User.objects.get(resetPasswordUUID=resetPasswordUUID);
        except User.DoesNotExist:
            return Response(**generateError('NOT_FOUND'));
        serializer = self.serializer_class(user, context={'request': request});
        milliseconds_since_epoch = datetime.datetime.now().timestamp() * 1000;
        if int(milliseconds_since_epoch) > serializer.data['resetPasswordDate']:
            return Response(**generateError('EXPIRED'));
        updateSerializer = self.serializer_class(user, data={'password': password, 'resetPasswordDate': None, 'resetPasswordUUID': None}, context={'request': request},partial=True);
        updateSerializer.is_valid(raise_exception=True);
        updateSerializer.save();
        serializer = UserSerializer(updateSerializer.instance, context={'request': request});
        return Response(data=generateAuthInfo(user, serializer.data), status=status.HTTP_200_OK);


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class SendMailAPIView(APIView):

    def post(self, request):

        serializers = SendMailSerializer(data=request.data)
        if serializers.is_valid():
            first_name = serializers.validated_data.get('first_name')
            last_name = serializers.validated_data.get('last_name')
            email = serializers.validated_data.get('email')
            message = serializers.validated_data.get('message')
            send_mail('',  from_email=None, message=f'{first_name} {last_name} {email} {message}', recipient_list=['suppor-temir@mail.ru'])
            return Response(serializers.errors, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMailUserApiView(APIView):

    def post(self, request):

        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            mobile = serializer.validated_data.get('mobile')
            email = serializer.validated_data.get('email')

            city = serializer.validated_data.get('city')
            street = serializer.validated_data.get('street')
            building_name = serializer.validated_data.get('building_name')
            unit = serializer.validated_data.get('unit')
            description = serializer.validated_data.get('description')
            message = serializer.validated_data.get('message')
            send_mail('', from_email=None, message=f' first name: {first_name}\n last name: {last_name}\n email: {email}\n message: {message}\n mobile: {mobile}\n city: {city}\n street: {street}\n building name:  {building_name}\n unit:  {unit}\n description: {description}\n',
                      recipient_list=['temircard@gmail.com'])
            return Response(serializer.errors, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasketCreateListView(generics.ListCreateAPIView):
    # serializer = BasketSerializer
    queryset = Basket.objects.all()
    

class BasketDeteleView(generics.DestroyAPIView):
    # serializer = BasketSerializer
    queryset = Basket.objects.all()


class MycardCreateListView(generics.ListCreateAPIView):
    # serializer = BasketSerializer
    queryset = Mycard.objects.all()
    

class MycardDeteleView(generics.DestroyAPIView):
    # serializer = BasketSerializer
    queryset = Mycard.objects.all()
    

class BankcardCreateListView(generics.ListCreateAPIView):
    # serializer = BasketSerializer
    queryset = Bankcard.objects.all()


class BankcardDeteleView(generics.DestroyAPIView):
    # serializer = BasketSerializer
    queryset = Bankcard.objects.all()
    
    
class SubscrCreateListView(generics.ListCreateAPIView):
    # serializer = BasketSerializer
    queryset = Subscr.objects.all()


class SubscrDeteleView(generics.DestroyAPIView):
    # serializer = BasketSerializer
    queryset = Subscr.objects.all()
    
    
class ComentCreateListView(generics.ListCreateAPIView):
    # serializer = BasketSerializer
    queryset = Coment.objects.all()


class ComentDeteleView(generics.DestroyAPIView):
    # serializer = BasketSerializer
    queryset = Coment.objects.all()


# class LikeCreateListView(generics.ListCreateAPIView):
#     # serializer = BasketSerializer
#     queryset = Like.objects.all()
    
# class LikeDeteleView(generics.DestroyAPIView):
#     # serializer = BasketSerializer
#     queryset = Like.objects.all()
    
    
class FavoritesCreateListView(generics.ListCreateAPIView):
    # serializer = BasketSerializer
    queryset = Favorites.objects.all()


class FavoritesDeteleView(generics.DestroyAPIView):
    # serializer = BasketSerializer
    queryset = Favorites.objects.all()

     
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

    
class AddLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            Likes.objects.get(ip=ip_client, pos_id=pk)
            return redirect(f'/{pk}')
        except:
            new_like = Likes()
            new_like.ip = ip_client
            new_like.pos_id = int(pk)
            new_like.save()
            return redirect(f'/{pk}')


class DelLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            lik = Likes.objects.get(ip=ip_client)
            lik.delete()
            return redirect(f'/{pk}')
        except:
            return redirect(f'/{pk}')


class BasicUserRegistrationView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type="object",
        properties={
            "name": openapi.Schema(type="string", example="Bilal"),
            "user_type": openapi.Schema(type="integer", example=1),
            "last_name": openapi.Schema(type="string", example="Kubatbekov"),
            "email": openapi.Schema(type="string", example="azbk2004@gmail.com"),
            "phone_number": openapi.Schema(type="string", example="996770519040"),
            "password": openapi.Schema(type="string", example="admin"),
        }
    ))
    def post(self, request, format=None):
        serializer = BasicUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerRegistrationView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type="object",
        properties={
            "name": openapi.Schema(type="string", example="BilalHolding"),
            "email": openapi.Schema(type="string", example="partner@partner.com"),
            "user_type": openapi.Schema(type="integer", example=2),
            "address": openapi.Schema(type="string", example="Bishkek"),
            "org": openapi.Schema(type="string", example="OcOO"),
            "inn": openapi.Schema(type="string", example="123456789"),
            "activity_type": openapi.Schema(type="string", example="Автосалон"),
            "description": openapi.Schema(type="string", example="Overall we are the best"),
            "phone_one": openapi.Schema(type="string", example="996519040"),
            "password": openapi.Schema(type="string", example="admin"),
        }
    ))
    def post(self, request, format=None):
        serializer = PartnerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
