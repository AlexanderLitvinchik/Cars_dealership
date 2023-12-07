from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecificationViewSet, ShowroomViewSet

router = DefaultRouter()
router.register(r'specifications', SpecificationViewSet)
router.register(r'', ShowroomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
