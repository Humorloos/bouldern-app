"""This file contains custom model manager classes"""
from django.db.models import Manager


class UGCManager(Manager):
    """
    Manager class for UGC model
    """

    def deactivate_all(self, user):
        """
        Sets all active instances inactive
        """
        self.active().update(is_active=False, modified_by=user)

    def active(self):
        """
        Gets all active instances
        :return: QuerySet of all active instances
        """
        return self.filter(is_active=True)
