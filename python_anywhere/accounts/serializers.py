"""Serializers for accounts app"""
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer

from python_anywhere.accounts.models import User


class UserSerializer(ModelSerializer):
    """Serializer for User instances"""

    class Meta:
        model = User
        fields = ['username', 'email', 'id', 'is_active']
        extra_kwargs = {
            'is_active': {'write_only': True}
        }


class LowerCaseEmailField(EmailField):
    """Email field that transforms values to lower case when deserializing"""
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return internal_value.lower()


class CustomRegisterSerializer(RegisterSerializer):
    """Serializer for transforming emails to lower case during registration"""

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = LowerCaseEmailField(required=True)


class CustomLoginSerializer(LoginSerializer):
    """Serializer for transforming emails to lower case during login"""

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = LowerCaseEmailField(required=True)
