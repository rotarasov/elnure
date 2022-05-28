from rest_framework.routers import DefaultRouter

from elnure_core import views


router = DefaultRouter(trailing_slash=False)

router.register("instructors", views.InstructorViewSet, basename="instructor")
router.register("blocks", views.BlockViewSet, basename="block")
router.register(
    "elective-courses", views.ElectiveCourseViewSet, basename="elective-course"
)
router.register("choices", views.ChoiceViewSet, basename="choice")

urlpatterns = router.urls
