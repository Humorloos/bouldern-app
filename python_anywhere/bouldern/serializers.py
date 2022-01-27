"""Serializers for the bouldern app"""
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from python_anywhere.bouldern.models import Gym, Color, DifficultyLevel, Boulder


class ColorSerializer(ModelSerializer):
    """Serializer for Color instances"""

    class Meta:
        model = Color
        fields = ['name', 'color', 'id']


class DifficultyLevelSerializer(ModelSerializer):
    """Serializer for DifficultyLevel instances"""
    color = ColorSerializer(read_only=True)
    color_id = PrimaryKeyRelatedField(source='color',
                                      queryset=Color.objects.all())

    class Meta:
        model = DifficultyLevel
        fields = ['level', 'color', 'color_id', 'id']


class BoulderSerializer(ModelSerializer):
    """Serializer for Color instances"""
    color = ColorSerializer(read_only=True)
    color_id = PrimaryKeyRelatedField(source='color',
                                      queryset=Color.objects.all())
    difficulty = DifficultyLevelSerializer(read_only=True)
    difficulty_id = PrimaryKeyRelatedField(
        source='difficulty', queryset=DifficultyLevel.objects.all())

    class Meta:
        model = Boulder
        fields = [
            'coordinates', 'gym', 'id', 'color', 'color_id', 'difficulty',
            'difficulty_id', 'is_active']
        extra_kwargs = {
            'is_active': {'write_only': True}
        }


class GymSerializer(ModelSerializer):
    """Serializer for Gym instances"""
    difficultylevel_set = DifficultyLevelSerializer(many=True)
    boulder_set = BoulderSerializer(many=True, required=False)

    class Meta:
        model = Gym
        fields = ['name', 'map', 'id', 'difficultylevel_set', 'boulder_set']

    def create(self, validated_data):
        difficultylevel_set_data = validated_data.pop('difficultylevel_set')
        gym = Gym.objects.create(**validated_data)
        for difficulty_level_data in difficultylevel_set_data:
            DifficultyLevel.objects.create(
                gym=gym, created_by=validated_data['created_by'],
                **difficulty_level_data)
        return gym
