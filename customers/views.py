from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (JWTAuthentication,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
