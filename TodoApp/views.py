from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterSerializer, TodoSerializer
from .models import Task
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from datetime import timedelta, datetime
import jwt
from .authenticate import CustomAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        MySerializer = RegisterSerializer(data=request.data)
        if MySerializer.is_valid():
            MySerializer.save()
            return Response(MySerializer.data, status=status.HTTP_201_CREATED)
        return Response(MySerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)  # Corrected typo here
            if not user.check_password(password):
                return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            secret_key = "This_is_secret_key"
            payload = {
                "user_id": user.id,
                "name": user.username,
                "exp": datetime.now() + timedelta(hours=1)  # Corrected the datetime usage
            }
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            return Response({"access_token": token}, status=status.HTTP_200_OK)  # No need to cast to str
        except User.DoesNotExist:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class TodoView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Fetch todos for the logged-in user
        todos = Task.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)


class TodoDetailView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Fetch todo for the logged-in user
            todo = Task.objects.get(id=pk, user=request.user)
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"Item does not exist"}, status=status.HTTP_404_NOT_FOUND)
