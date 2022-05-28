from rest_framework.routers import DefaultRouter

from elnure_config import views


router = DefaultRouter(trailing_slash=False)

router.register("appwindows", views.ApplicationWindowViewSet, basename="appwindow")

urlpatterns = router.urls
