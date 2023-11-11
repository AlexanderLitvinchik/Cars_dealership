from django.shortcuts import render

from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import Customer
from .models import Specification, Showroom, \
    ShowroomCarRelationship, Car, ShowroomDiscount
from .serializers import SpecificationSerializer, ShowroomDiscountSerializer, \
    CarSerializer, ShowroomSerializer, ShowroomCarRelationshipSerializer, ShowroomHistorySerializer


class ShowroomViewSet(viewsets.ModelViewSet):
    queryset = Showroom.objects.all()
    serializer_class = ShowroomSerializer
    # Переопределите права доступа по необходимости
    # permission_classes = [IsAuthenticated,]
    """
    Created views for showroom
    """

    @action(detail=True, methods=["GET"])
    def cars(self, request, pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        cars = showroom.car.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def add_car(self, request, pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        data = request.data
        data['showroom'] = pk
        serializer = ShowroomCarRelationshipSerializer(data=data)
        car = get_object_or_404(Car, pk=data['car'])
        if serializer.is_valid():
            serializer.save()
            showroom.car.add(serializer.data['car'])
            car.showrooms.add(serializer.data['showroom'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # не уверен вообще, что стоит писать  запросы на удаление(есть поле is_active) и изменение ?
    @action(detail=True, methods=["DELETE"])
    def remove_car(self, request,  pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        car = request.data.get('car')
        try:
            car = showroom.car.get(pk=car)
            showroom.car.remove(car)
            return Response({'detail': 'Car removed from showroom.'})
        except Car.DoesNotExist:
            return Response({'detail': 'Car not found in showroom.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["PUT"])
    def update_car(self, request,  pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        car = request.data.get('car')
        try:
            car_relationship = ShowroomCarRelationship.objects.get(
                showroom=showroom,
                car=car
            )
        except ShowroomCarRelationship.DoesNotExist:
            return Response({'detail': 'Car relationship not found in showroom.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShowroomCarRelationshipSerializer(car_relationship, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def history(self, request,  pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        history = showroom.showroom_histories.all()
        serializer = ShowroomHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def create_history(self, request, pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        data = request.data
        data['showroom'] = showroom.id
        serializer = ShowroomHistorySerializer(data=data)
        customer = get_object_or_404(Customer, pk=data['unique_customer'])
        if serializer.is_valid():
            instance = serializer.save()
            showroom.showroom_histories.add(instance)
            customer.customer_histories.add(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def discounts(self, request,  pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        discounts = showroom.discount_showroom.all()
        serializer = ShowroomDiscountSerializer(discounts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def create_discount(self, request,  pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        data = request.data
        serializer = ShowroomDiscountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            showroom.discount_showroom.add(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # получается хочу поменять скидку для одного автосалона а получается меняю для всех
    @action(detail=True, methods=["PUT"])
    def update_discounts(self, request,  pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        data = request.data
        discount_id = data['id']
        try:
            discount_showroom = ShowroomDiscount.objects.get(id=discount_id)
        except ShowroomDiscount.DoesNotExist:
            return Response({'detail': 'DiscountShowroom не найден.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShowroomDiscountSerializer(discount_showroom, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def specifications(self, request, pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        specifications = showroom.specifications.all()
        serializer = SpecificationSerializer(specifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def add_specification(self, request,  pk: int = None) -> Response:
        showroom = get_object_or_404(Showroom, pk=pk)
        data = request.data
        serializer = SpecificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            showroom.specifications.add(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    # permission_classes = [IsAuthenticated, ]
