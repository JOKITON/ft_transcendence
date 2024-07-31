from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Do not include password

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Check if the username already exists
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})
        
        # Check if the email already exists
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})

        return data

    def create(self, validated_data):
        # Create and return a new user instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        # Check if both username and password are provided
        if not username or not password:
            raise serializers.ValidationError('Both username and password are required.')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        # Check if authentication was successful
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        
        return {
            'user': user
        }