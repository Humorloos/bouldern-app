"""URL mappings for accounts app"""

# accounts/urls.py
from rest_framework.routers import SimpleRouter

from python_anywhere.accounts.views import UserAPI

router = SimpleRouter()
router.register(UserAPI.basename, UserAPI)
urlpatterns = router.urls
