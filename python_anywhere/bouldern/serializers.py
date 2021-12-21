from rest_framework.serializers import ModelSerializer

from python_anywhere.bouldern.models import Gym


class UGCSerializer(ModelSerializer):
    def save(self, user):
        ugc = super().save()
        ugc.created_by = user
        ugc.save()


class GymSerializer(UGCSerializer):
    class Meta:
        model = Gym
        fields = ['name', 'map']
