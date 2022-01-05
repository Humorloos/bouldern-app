from rest_framework.serializers import ModelSerializer

from python_anywhere.accounts.models import User


class UserSerializer(ModelSerializer):
    """Serializer for User instances"""

    class Meta:
        model = User
        fields = ['username', 'email']
