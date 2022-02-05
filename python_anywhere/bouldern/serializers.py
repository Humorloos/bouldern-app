"""Serializers for the bouldern app"""
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from python_anywhere.bouldern.models import Gym, Color, Grade, \
    Boulder, Ascent


class ColorSerializer(ModelSerializer):
    """Serializer for Color instances"""

    class Meta:
        model = Color
        fields = ['name', 'color', 'id']


class GradeSerializer(ModelSerializer):
    """Serializer for Grade instances"""
    color = ColorSerializer(read_only=True)
    color_id = PrimaryKeyRelatedField(source='color',
                                      queryset=Color.objects.all())

    class Meta:
        model = Grade
        fields = ['grade', 'color', 'color_id', 'id']


class BoulderSerializer(ModelSerializer):
    """Serializer for Color instances"""
    color = ColorSerializer(read_only=True)
    color_id = PrimaryKeyRelatedField(source='color',
                                      queryset=Color.objects.all())
    grade = GradeSerializer(read_only=True)
    grade_id = PrimaryKeyRelatedField(
        source='grade', queryset=Grade.objects.all())

    class Meta:
        model = Boulder
        fields = [
            'coordinates', 'gym', 'id', 'color', 'color_id', 'grade',
            'grade_id', 'is_active']
        extra_kwargs = {
            'is_active': {'write_only': True}
        }


class GymSerializer(ModelSerializer):
    """Serializer for Gym instances"""
    grade_set = GradeSerializer(many=True)

    class Meta:
        model = Gym
        fields = ['name', 'map', 'id', 'grade_set']

    def create(self, validated_data):
        grade_set_data = validated_data.pop('grade_set')
        gym = Gym.objects.create(**validated_data)
        for grade_data in grade_set_data:
            Grade.objects.create(
                gym=gym, created_by=validated_data['created_by'],
                **grade_data)
        return gym


class AscentSerializer(ModelSerializer):
    """Serializer for Ascent instances"""
    boulder = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ascent
        fields = ['result', 'id', 'boulder']
