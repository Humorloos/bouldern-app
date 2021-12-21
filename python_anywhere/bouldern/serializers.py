"""Serializers for the bouldern app"""
from rest_framework.serializers import ModelSerializer

from python_anywhere.bouldern.models import Gym, Color


class UGCSerializer(ModelSerializer):
    """Abstract serializer for serializing UGC Models"""
    def save(self, user):
        ugc = super().save()
        ugc.created_by = user
        ugc.save()


class GymSerializer(UGCSerializer):
    """Serializer for Gym instances"""
    class Meta:
        model = Gym
        fields = ['name', 'map']


class ColorSerializer(UGCSerializer):
    """Serializer for Color instances"""
    class Meta:
        model = Color
        fields = ['name', 'color']
