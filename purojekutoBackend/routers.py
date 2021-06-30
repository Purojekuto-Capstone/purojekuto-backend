from rest_framework.routers import DefaultRouter
from apps.activities.api.views.activities_views import (
    ActivityViewSet,
    ActivityCategoryViewSet,
)
from apps.projects.api.views.projects_views import (
    ProjectViewSet,
    ProjectCategoryViewSet,
)
from apps.projects.api.views.metrics_views import (
    ProgressViewSet,
    MetricsViewSet,
)

router = DefaultRouter()

router.register(
    r"project_category", ProjectCategoryViewSet, basename="project_category"
)
router.register(
    r"activity_category", ActivityCategoryViewSet, basename="activity_category"
)
router.register(r"project", ProjectViewSet, basename="project")
router.register(r"activity", ActivityViewSet, basename="activity")
router.register(r"progress", ProgressViewSet, basename="progress")
router.register(r"metrics", MetricsViewSet, basename="metrics")

urlpatterns = router.urls
