from rest_framework import serializers
from accounts.models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
  
    class Meta:
        model = CustomUser
        fields = ('password','first_name','last_name','password1','email','email_verified')
    
    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('email already exists!')
        return value

    def validate(self,attrs):
        if attrs['password']!=attrs['password1']:
            raise serializers.ValidationError('password and password1 didn\'t match')
        return attrs
    
       
    def create(self,validated_data):
        password1 = validated_data.pop('password1')
        user = CustomUser(first_name=validated_data.get('first_name',''),
        last_name = validated_data.get('last_name',''),
        email = validated_data['email'])
        user.set_password(password1)
        user.save()
        return user

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=10)