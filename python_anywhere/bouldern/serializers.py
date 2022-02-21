"""Serializers for the bouldern app"""
from rest_framework.fields import SerializerMethodField, ModelField
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from python_anywhere.bouldern.models import Gym, Color, Grade, \
    Boulder, Ascent, FavoriteGym


class ColorSerializer(ModelSerializer):
    """Serializer for Color instances"""

    class Meta:
        model = Color
        fields = ['name', 'color', 'id']


class GradeField(ModelField):
    def to_representation(self, value):
        if value.grade is None:
            return 'undefined'
        return value.grade

    def to_internal_value(self, data):
        if data == "undefined":
            data = None
        return super().to_internal_value(data)


class GradeSerializer(ModelSerializer):
    """Serializer for Grade instances"""
    color = PrimaryKeyRelatedField(queryset=Color.objects.all())
    grade = GradeField(model_field=Grade()._meta.get_field('grade'),
                       allow_null=True)

    class Meta:
        model = Grade
        fields = ['grade', 'color', 'id']


class BoulderSerializer(ModelSerializer):
    """Serializer for Color instances"""
    color = PrimaryKeyRelatedField(queryset=Color.objects.all())
    grade = PrimaryKeyRelatedField(queryset=Grade.objects.all())

    class Meta:
        model = Boulder
        fields = ['coordinates', 'id', 'color', 'grade', 'age', 'is_active']
        extra_kwargs = {
            'is_active': {'write_only': True}
        }


class GymSerializer(ModelSerializer):
    """Serializer for Gym instances"""
    grade_set = SerializerMethodField()

    class Meta:
        model = Gym
        fields = ['name', 'map', 'id', 'grade_set']

    def get_grade_set(self, obj):
        return GradeSerializer(obj.grade_set.filter(is_active=True), many=True) \
            .data

    def create(self, validated_data):
        grade_set_data = validated_data.pop('grade_set')
        gym = Gym.objects.create(**validated_data)
        for grade_data in grade_set_data:
            Grade.objects.create(
                gym=gym, created_by=validated_data['created_by'],
                **grade_data)
        return gym

    def update(self, instance, validated_data):
        grade_set_data = self.initial_data['grade_set']
        original_grade_set = {
            grade.pk: grade for grade in instance.grade_set.filter(
                is_active=True)
        }
        user = validated_data['modified_by']
        for grade_data in grade_set_data:
            grade_serializer = GradeSerializer(data=grade_data)
            grade_serializer.is_valid(raise_exception=True)
            validated_grade_data = grade_serializer.validated_data
            # If grade has id and it's different from existing grade with this
            # id, update it
            if 'id' in grade_data:
                grade_id = grade_data['id']
                grade = original_grade_set.pop(grade_id)
                original_grade_data = {
                    key: getattr(grade, key)
                    for key in validated_grade_data.keys()
                }
                if validated_grade_data != original_grade_data:
                    grade.modified_by = user
                    for key, value in validated_grade_data.items():
                        setattr(grade, key, value)
                    grade.save()
            # If grade does not have id, modify inactive existing grade or
            # create a new one
            else:
                grade, created = instance.grade_set.update_or_create(
                    is_active=False,
                    gym=instance,
                    grade=validated_grade_data['grade'],
                    defaults={
                        'is_active': True,
                        'color': validated_grade_data['color'],
                        'modified_by': user
                    }
                )
                if created:
                    grade.created_by = user
                grade.save()
        # deactivate grades that are missing in grade set together with
        # corresponding boulders
        for grade in original_grade_set.values():
            grade.is_active = False
            grade.modified_by = user
            grade.save()
            grade.boulder_set.update(is_active=False)
        return instance


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


class FavoriteGymSerializer(ModelSerializer):
    """Serializer for favorite gym instances"""
    gym = StringRelatedField()

    class Meta:
        model = FavoriteGym
        fields = ['gym']
