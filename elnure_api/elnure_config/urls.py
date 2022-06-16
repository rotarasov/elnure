from django.urls import path
from rest_framework.routers import DefaultRouter

from elnure_config import views


router = DefaultRouter(trailing_slash=False)

router.register("appwindows", views.ApplicationWindowViewSet, basename="appwindow")
router.register(
    "ref/appwindows",
    views.RefApplicationWindowViewSet,
    basename="ref-appwindow",
)

urlpatterns = router.urls
