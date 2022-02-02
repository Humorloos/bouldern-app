"""URL mappings for bouldern app"""
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from python_anywhere.bouldern.views import GymAPI, ColorAPI, BoulderAPI, \
    AscentAPI

router = SimpleRouter()
router.register(GymAPI.basename, GymAPI)
router.register(ColorAPI.basename, ColorAPI)
router.register(BoulderAPI.basename, BoulderAPI)

gym_router = NestedSimpleRouter(router, GymAPI.basename,
                                lookup=GymAPI.basename)
gym_router.register(BoulderAPI.basename, BoulderAPI)

boulder_router = NestedSimpleRouter(gym_router, BoulderAPI.basename,
                                    lookup=BoulderAPI.basename)
boulder_router.register(AscentAPI.basename, AscentAPI)

urlpatterns = router.urls + gym_router.urls + boulder_router.urls
