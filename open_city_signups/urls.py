from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from signups.api import SignupTargetViewSet, SignupViewSet

router = routers.DefaultRouter()
router.register('signup', SignupViewSet)
router.register('signup_target', SignupTargetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
]
