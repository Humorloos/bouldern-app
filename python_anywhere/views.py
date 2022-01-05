from django.utils.decorators import classonlymethod
from rest_framework.viewsets import GenericViewSet


class ReversibleViewSet(GenericViewSet):
    """
    VewSet base class that allows using ViewSet().reverse_action() for
    retrieving view URLs.
    """
    basename = None
    request = None

    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        basename = cls.basename
        view = super().as_view(actions, **initkwargs)
        cls.basename = basename
        return view
