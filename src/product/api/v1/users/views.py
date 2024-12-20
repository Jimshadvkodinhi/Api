from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import SignUpSerializer, LoginSerializer, UserTokenObtainPairSerializer
from users.models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from api.v1.users.serializers import *


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        phone = serializer.validated_data['phone']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({
                "StatusCode": 6001,
                "title": "Failed!",
                "message": "Username already exists!",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if phone already exists
        if UserProfile.objects.filter(phone=phone).exists():
            return Response({
                "StatusCode": 6001,
                "title": "Failed!",
                "message": "Phone number already registered!",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create User and UserProfile
        try:
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, phone=phone)
            return Response({
                "StatusCode": 6000,
                "title": "Success",
                "message": "User registered successfully",
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "StatusCode": 6002,
                "title": "Failed!",
                "message": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            "StatusCode": 6001,
            "title": "Failed!",
            "message": "Invalid data!",
            "errors": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        try:
            user_profile = UserProfile.objects.get(phone=phone)
            user = authenticate(username=user_profile.user.username, password=password)

            if user:
                # Generate tokens for the user
                refresh = RefreshToken.for_user(user)
                return Response({
                    "StatusCode": 6000,
                    "message": "Login successful",
                    "token_data": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "StatusCode": 6001,
                    "message": "Incorrect phone number or password!",
                }, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return Response({
                "StatusCode": 6001,
                "message": "User not found!",
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            "StatusCode": 6002,
            "message": "Invalid data!",
            "errors": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if request.method == 'GET':
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Profile updated successfully", "data": serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)