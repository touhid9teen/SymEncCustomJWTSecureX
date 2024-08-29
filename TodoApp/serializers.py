from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        return Task.objects.create(**validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','email', 'password']

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError({'username': 'This username is already taken.'})

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({'email': 'This email is alreadyn registerd.'})
        
        return  data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 