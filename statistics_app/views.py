from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from autosalons.models import Showroom, Car
from customers.models import Customer
from suppliers.models import Supplier
from .collector import get_showroom_stat, get_supplier_stat, get_customer_stat
from .serializers import ShowroomStatisticsSerializer, SupplierStatisticsSerializer, CustomerStatisticsSerializer


class ShowroomStatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet to retrieve statistics for showrooms.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def list(self, request) -> Response:
        showrooms = Showroom.objects.all()
        showroom_statistics = [get_showroom_stat(showroom) for showroom in showrooms]

        serializer = ShowroomStatisticsSerializer(showroom_statistics, many=True)
        if not serializer:
            raise ValidationError("Wrong statistics data!")
        return Response(serializer.data)


class SupplierStatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet to retrieve statistics for suppliers.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def list(self, request) -> Response:
        suppliers = Supplier.objects.all()
        supplier_statistics = [get_supplier_stat(supplier) for supplier in suppliers]

        serializer = SupplierStatisticsSerializer(supplier_statistics, many=True)
        if not serializer:
            raise ValidationError("Wrong statistics data!")
        return Response(serializer.data)


class CustomerStatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet to retrieve statistics for customers.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def list(self, request) -> Response:
        customers = Customer.objects.all()
        customer_statistics = [get_customer_stat(customer) for customer in customers]

        serializer = CustomerStatisticsSerializer(customer_statistics, many=True)
        if not serializer:
            raise ValidationError("Wrong statistics data!")
        return Response(serializer.data)
