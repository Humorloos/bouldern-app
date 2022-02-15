"""Serializers for accounts app"""
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
