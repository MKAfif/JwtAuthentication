from rest_framework import serializers
from app1.models import Customer

class RegisterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ("username","email","password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class LoginUserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Customer
        fields = ['email','username','profile_photo','is_superuser','is_active']


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Customer
        fields = ('id' ,'username', 'email' , 'profile_photo' )

class ImageupdateSerializer(serializers.ModelSerializer):

    profile_photo = serializers.ImageField()
    class Meta:
        model   = Customer
        fields  = ('profile_photo')