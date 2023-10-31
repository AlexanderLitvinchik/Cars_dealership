from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from autosalons.models import Supplier_Specification_price
from autosalons.serializers import SupplierSpecificationPriceSerializer

from .models import Supplier_Discount, Sales_of_suppliers
from .serializers import SupplierDiscountSerializer, SalesOfSuppliersSerializer


class SupplierDiscountListCreateView(generics.ListCreateAPIView):
    queryset = Supplier_Discount.objects.all()
    serializer_class = SupplierDiscountSerializer


class SupplierDiscountUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Supplier_Discount.objects.all()
    serializer_class = SupplierDiscountSerializer


class SalesOfSuppliersListCreateView(generics.ListCreateAPIView):
    queryset = Sales_of_suppliers.objects.all()
    serializer_class = SalesOfSuppliersSerializer


class SalesOfSuppliersUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Sales_of_suppliers.objects.all()
    serializer_class = SalesOfSuppliersSerializer


class SupplierSpecificationPriceListCreateView(generics.ListCreateAPIView):
    queryset = Supplier_Specification_price.objects.all()
    serializer_class = SupplierSpecificationPriceSerializer


class SupplierSpecificationPriceUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Supplier_Specification_price.objects.all()
    serializer_class = SupplierSpecificationPriceSerializer


class SupplierSpecificationPriceAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            price = Supplier_Specification_price.objects.get(pk=pk)
            serializer = SupplierSpecificationPriceSerializer(price)
            return Response(serializer.data)
        else:
            prices = Supplier_Specification_price.objects.all()
            serializer = SupplierSpecificationPriceSerializer(prices, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = SupplierSpecificationPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        price = Supplier_Specification_price.objects.get(pk=pk)
        serializer = SupplierSpecificationPriceSerializer(price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
