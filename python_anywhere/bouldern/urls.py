"""URL mappings for bouldern app"""
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from python_anywhere.bouldern.views import GymAPI, ColorAPI, BoulderAPI

router = SimpleRouter()
router.register(GymAPI.basename, GymAPI)
router.register(ColorAPI.basename, ColorAPI)

gym_router = NestedSimpleRouter(router, GymAPI.basename,
                                lookup=GymAPI.basename)
gym_router.register(BoulderAPI.basename, BoulderAPI)

urlpatterns = router.urls + gym_router.urls
