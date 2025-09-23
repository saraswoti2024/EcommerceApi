from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from accounts.models import CustomUser
from .serializers import RegistrationSerializer,VerifySerializer
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.emails import opt_email

class RegisterView(APIView):
    def post(self,request):
        try:
            serializers_class = RegistrationSerializer(data=request.data)
            if serializers_class.is_valid():
                serializers_class.save()
                opt_email(serializers_class.data['email'])
                return Response(serializers_class.data,status=status.HTTP_201_CREATED)
            return Response({'message_response': serializers_class.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message_error' : f'{str(e)}'},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            data = CustomUser.objects.all()
            datas = RegistrationSerializer(data,many=True)
            return Response(datas.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message_exception':f'{str(e)}'},status=status.HTTP_400_BAD_REQUEST)

class VerifyOtp(APIView):
    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            # Safely get user
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {'message_response': "User doesn't exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Compare OTP stored on user model
            if str(user.otp) != str(otp):
                return Response(
                    {'message_response': 'OTP is incorrect'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Mark as verified
            user.email_verified = True
            user.save()

            return Response(
                {'message_response': 'Verified email'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
