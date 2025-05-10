# accounts/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from rest_framework.authtoken.models import Token
from .serializers import (UserRegistrationSerializer, UserProfileSerializer, CustomUserSerializer
                    , LoginSerializer, ProfileUpdateSerializer, ChangePasswordSerializer)
from accounts.models import CustomUser


class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserProfileSerializer(user).data,
            "token": token.key
        })


class LogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserProfileSerializer(user).data,
            "token": token.key
        })

class ProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserListAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

class UserRetrieveAPI(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

class ProfileUpdateAPI(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(UserProfileSerializer(instance).data)

class ChangePasswordAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Optional: Revoke existing token and create new one
        Token.objects.filter(user=user).delete()
        new_token = Token.objects.create(user=user)
        
        return Response({
            "message": "Password changed successfully",
            "new_token": new_token.key
        })

class DeleteUserAPI(APIView):
    permission_classes = [IsAdminUser]  # Only admins can delete users

    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=user_id)
            if user == request.user:
                return Response(
                    {"detail": "You cannot delete your own admin account."},
                    status=status.HTTP_403_FORBIDDEN
                )
            if user.is_superuser:
                return Response(
                    {"detail": "Superusers cannot be deleted via this API."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            Token.objects.filter(user=user).delete()
            user.delete()
            
            return Response(
                {"detail": f"User {user.username} deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

