"""Serializers for the bouldern app"""

from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from python_anywhere.bouldern.models import Gym, Color, Grade, \
    Boulder, Ascent


class ColorSerializer(ModelSerializer):
    """Serializer for Color instances"""

    class Meta:
        model = Color
        fields = ['name', 'color', 'id']


class GradeSerializer(ModelSerializer):
    """Serializer for Grade instances"""
    color = PrimaryKeyRelatedField(queryset=Color.objects.all())

    class Meta:
        model = Grade
        fields = ['grade', 'color', 'id']


class BoulderSerializer(ModelSerializer):
    """Serializer for Color instances"""
    color = PrimaryKeyRelatedField(queryset=Color.objects.all())
    grade = PrimaryKeyRelatedField(queryset=Grade.objects.all())

    class Meta:
        model = Boulder
        fields = ['coordinates', 'id', 'color', 'grade', 'is_active']
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

    class Meta:
        model = Ascent
        fields = ['result']


class BoulderFeatureSerializer(Serializer):
    """
    Serializer for Boulder Features, consisting of a boulder and an ascent
    instance
    """

    boulder = BoulderSerializer()
    ascent = AscentSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class GymMapResourcesSerializer(Serializer):
    """
    Serializer for gym map resources which consist of a Gym instance and a
    collection of Boulder Feature instances
    """

    gym = GymSerializer()
    boulder_features = BoulderFeatureSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
