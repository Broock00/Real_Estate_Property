from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2', 'phone_number', 
                 'date_of_birth', 'profile_picture', 'bio', 'digital_id', 
                 'address', 'city', 'role')
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        if 'digital_id' in data and data['digital_id'] and CustomUser.objects.filter(digital_id=data['digital_id']).exists():
            raise serializers.ValidationError({"digital_id": "Digital ID already exists"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 
                 'profile_picture', 'bio', 'digital_id', 'address', 
                 'city', 'role')
        read_only_fields = ('digital_id', 'email', 'role')

# retrieve the users information
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'profile_picture', 'bio', 'digital_id', 'address', 'city', 'role'
        ]
        read_only_fields = fields

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_picture',
            'bio', 'digital_id', 'address', 'city', 'role'
        )
        extra_kwargs = {
            'username': {'required': False},
            'phone_number': {'required': False},
            'date_of_birth': {'required': False},
            'profile_picture': {'required': False},
            'bio': {'required': False},
            'address': {'required': False},
            'city': {'required': False}
        }
        read_only_fields = ('digital_id', 'role')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                              email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'")
            
        data['user'] = user
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is incorrect"})
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "New passwords must match"})
        if len(data['new_password']) < 8:
            raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long"})
        return data


