from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from autosalons.models import Showroom
from .models import SupplierDiscount, Supplier
from .serializers import SupplierDiscountSerializer, SupplierHistorySerializer, SupplierSerializer
from django.shortcuts import get_object_or_404


class SupplierViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = (JWTAuthentication,)
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    @action(detail=True, methods=["GET"])
    def history(self, request, pk: int = None) -> Response:
        supplier = get_object_or_404(Supplier, pk=pk)
        history = supplier.histories.all()
        serializer = SupplierHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def create_history(self, request, pk: int = None) -> Response:
        supplier = get_object_or_404(Supplier, pk=pk)
        data = request.data
        data['supplier'] = supplier.id
        serializer = SupplierHistorySerializer(data=data)
        showroom = get_object_or_404(Showroom, pk=data['showroom'])
        if serializer.is_valid():
            instance = serializer.save()
            supplier.histories.add(instance)
            showroom.histories_of_suppliers_to_showroom.add(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # put запросы писать наверно не логично , так как вроде история покупок не должна меняться
    @action(detail=True, methods=["GET"])
    def discounts(self, request, pk: int = None) -> Response:
        supplier = get_object_or_404(Supplier, pk=pk)
        discounts = supplier.discount_suppliers.all()
        serializer = SupplierDiscountSerializer(discounts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def create_discount(self, request, pk: int = None) -> Response:
        supplier = get_object_or_404(Supplier, pk=pk)
        data = request.data
        data['supplier'] = supplier.id
        serializer = SupplierDiscountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            supplier.discount_suppliers.add(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["PUT"])
    def update_discounts(self, request, pk: int = None) -> Response:
        supplier = get_object_or_404(Supplier, pk=pk)
        data = request.data
        discount_id = data['id']
        try:
            supplier_discount = SupplierDiscount.objects.get(id=discount_id)
        except SupplierDiscount.DoesNotExist:
            return Response({'detail': 'SupplierDiscount не найден.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SupplierDiscountSerializer(supplier_discount, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
