"""Serializers for the bouldern app"""
from rest_framework.serializers import ModelSerializer

from python_anywhere.bouldern.models import Gym, Color, DifficultyLevel, Boulder


class DifficultyLevelSerializer(ModelSerializer):
    """Serializer for DifficultyLevel instances"""

    class Meta:
        model = DifficultyLevel
        fields = ['level', 'color']


class GymSerializer(ModelSerializer):
    """Serializer for Gym instances"""
    difficultylevel_set = DifficultyLevelSerializer(many=True)

    class Meta:
        model = Gym
        fields = ['name', 'map', 'id', 'difficultylevel_set']

    def create(self, validated_data):
        difficultylevel_set_data = validated_data.pop('difficultylevel_set')
        gym = Gym.objects.create(**validated_data)
        for difficulty_level_data in difficultylevel_set_data:
            DifficultyLevel.objects.create(
                gym=gym, created_by=validated_data['created_by'],
                **difficulty_level_data)
        return gym


class ColorSerializer(ModelSerializer):
    """Serializer for Color instances"""

    class Meta:
        model = Color
        fields = ['name', 'color', 'id']


class BoulderSerializer(ModelSerializer):
    """Serializer for Color instances"""

    class Meta:
        model = Boulder
        fields = ['coordinates', 'gym', 'id']
