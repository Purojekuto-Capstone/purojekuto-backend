from rest_framework.routers import DefaultRouter
from apps.projects.api.views.general_views import *

router = DefaultRouter()

router.register(r'project_category', ProjectCategoryViewSet, basename = 'project_category')
router.register(r'activity_category', ActivityCategoryViewSet, basename = 'activity_category')

urlpatterns = router.urls