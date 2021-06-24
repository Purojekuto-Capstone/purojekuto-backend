from rest_framework.routers import DefaultRouter
from apps.projects.api.views.general_views import *
from apps.projects.api.views.activities_views import *
from apps.projects.api.views.projects_views import *

router = DefaultRouter()

router.register(r'project_category', ProjectCategoryViewSet, basename = 'project_category')
router.register(r'activity_category', ActivityCategoryViewSet, basename = 'activity_category')
router.register(r'project', ProjectViewSet, basename = 'project')
router.register(r'activity', ActivityViewSet, basename = 'activity')
router.register(r'progress', ProgressViewSet, basename = 'progress')

urlpatterns = router.urls