from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    def post(self,request):
        try:
            serializers_class = RegistrationSerializer(data=request.data)
               
            if serializers_class.is_valid():
                serializers_class.save()
                return Response({'message': 'Registered Successfully!'},status=status.HTTP_201_CREATED)
            return Response({'message_response': serializers_class.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message_error' : f'{str(e)}'},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            data = User.objects.all()
            datas = RegistrationSerializer(data,many=True)
            return Response(datas.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message_exception':f'{str(e)}'},status=status.HTTP_400_BAD_REQUEST)