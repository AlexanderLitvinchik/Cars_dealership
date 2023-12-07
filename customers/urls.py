from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, register, confirm_registration,  reset_password

router = DefaultRouter()
router.register(r'', CustomerViewSet)

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm-registration/', confirm_registration, name='confirm_registration'),
    path('reset-password/', reset_password, name='reset_password'),
    path('', include(router.urls)),

]
