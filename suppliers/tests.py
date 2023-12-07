import json
import random
from datetime import datetime
import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from autosalons.models import Showroom, Car, Specification
from suppliers.models import Supplier, SupplierDiscount, SupplierHistory
from suppliers.serializers import SupplierDiscountSerializer, SupplierHistorySerializer, SupplierSerializer
from django.contrib.auth.models import User
from ddf import G, F


@pytest.fixture
def authenticated_user():
    return G(User, username='testuser')


@pytest.fixture
def authenticated_client(authenticated_user):
    client = APIClient()
    access_token = AccessToken.for_user(authenticated_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


@pytest.fixture
def supplier_discount() -> SupplierDiscount:
    return G(SupplierDiscount, start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=7),
             discount_percentage=10)


@pytest.fixture
def supplier() -> Supplier:
    return G(Supplier, name='Тестовый поставщик', year_founded=2002)


@pytest.fixture
def showroom() -> Showroom:
    return G(Showroom, name='Test Showroom', location='Germany', balance=120000)


@pytest.fixture
def specification() -> Specification:
    return G(Specification, name_of_car='Default Specification', color='красный', mileage=20000)


@pytest.fixture
def car(specification) -> Car:
    return G(Car, specification=specification, serial_number=lambda x: str(random.randint(100000, 999999)))


@pytest.fixture
def supplier_history(showroom: Showroom, supplier: Supplier, specification: Specification) -> Supplier:
    supplier = G(Supplier)
    supplier_history_1 = G(SupplierHistory, car=G(Car, specification=specification, serial_number='1211173'), amount=4,
                           showroom=showroom, supplier=supplier)
    supplier_history_2 = G(SupplierHistory, car=G(Car, specification=specification, serial_number='6711189'), amount=13,
                           showroom=showroom, supplier=supplier)
    supplier.histories.add(supplier_history_1, supplier_history_2)

    return supplier


@pytest.fixture
def supplier_with_discounts() -> Supplier:
    supplier = G(Supplier, name='Test Supplier', year_founded=2002)

    discounts = [
        G(SupplierDiscount, start_date='2023-11-15', end_date='2023-12-15', discount_percentage=10.0),
        G(SupplierDiscount, start_date='2023-11-20', end_date='2023-12-20', discount_percentage=15.0)
    ]

    supplier.discount_suppliers.set(discounts)
    return supplier


"""
    Added fixtures for urls
"""


@pytest.fixture
def supplier_list_url() -> str:
    return reverse('suppliers:supplier-list')


@pytest.fixture
def supplier_detail_url(supplier: Supplier) -> str:
    return reverse('suppliers:supplier-detail', kwargs={'pk': supplier.pk})


@pytest.mark.django_db
class TestSupplierViewSet:

    def test_suppliers_action(self, authenticated_client: APIClient, supplier: Supplier,
                              supplier_list_url: str) -> None:
        """Test the action of retrieving suppliers."""
        response = authenticated_client.get(supplier_list_url)

        assert response.status_code == status.HTTP_200_OK
        serializer = SupplierSerializer(supplier)
        assert response.data[0] == serializer.data

    def test_add_supplier(self, authenticated_client: APIClient, supplier_list_url: str) -> None:
        """Test the addition of a new supplier."""
        data = {
            'name': 'Тестовый поставщик',
            'year_founded': 2009,
        }
        json_data = json.dumps(data)
        response = authenticated_client.post(
            supplier_list_url, data=json_data, content_type='application/json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Supplier.objects.filter(name='Тестовый поставщик', year_founded=2009).exists()

    def test_update_supplier(self, authenticated_client: APIClient, supplier: Supplier,
                             supplier_detail_url: str) -> None:
        """Test updating a supplier's information."""
        data = {
            'name': 'Тестовый обновленный поставщик',
            'year_founded': 2009,
        }
        response = authenticated_client.put(
            supplier_detail_url, data, format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert Supplier.objects.filter(
            name='Тестовый обновленный поставщик', year_founded=2009
        ).exists()

    def test_delete_supplier(self, authenticated_client: APIClient, supplier: Supplier,
                             supplier_detail_url: str) -> None:
        """Test deleting a supplier."""
        response = authenticated_client.delete(supplier_detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            Supplier.objects.get(pk=supplier.pk)

    def test_supplier_history(self, authenticated_client: APIClient, supplier_history) -> None:
        """Test the retrieval of a supplier's history."""
        supplier = supplier_history
        url = reverse('suppliers:supplier-history', kwargs={'pk': supplier.id})
        response = authenticated_client.get(url)
        history_list = list(supplier.histories.all())
        serializer = SupplierHistorySerializer(history_list, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_create_supplier_history(self, authenticated_client: APIClient, supplier,
                                     showroom, car) -> None:
        """Test the creation of a supplier's history."""
        supplier = supplier
        showroom = showroom
        car = car
        url = reverse('suppliers:supplier-create-history', kwargs={'pk': supplier.id})
        data = {
            'car': car.id,
            'amount': 50000,
            'showroom': showroom.id,
            'supplier': supplier.id
        }
        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert SupplierHistory.objects.filter(supplier=supplier, amount=50000, showroom=showroom, car=car).exists()

    def test_supplier_discounts(self, authenticated_client: APIClient,
                                supplier_with_discounts) -> None:
        """Test the retrieval of a supplier's discounts."""
        supplier = supplier_with_discounts
        url = reverse('suppliers:supplier-discounts', kwargs={'pk': supplier.id})
        response = authenticated_client.get(url)
        discounts = SupplierDiscount.objects.filter(discount_suppliers=supplier)
        serializer = SupplierDiscountSerializer(discounts, many=True)
        expected_data = serializer.data
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_create_supplier_discount(self, authenticated_client: APIClient, supplier) -> None:
        """Test the creation of a discount for a supplier."""
        supplier = supplier
        url = reverse('suppliers:supplier-create-discount', kwargs={'pk': supplier.id})
        data = {
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'discount_percentage': 37
        }
        response = authenticated_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert SupplierDiscount.objects.filter(discount_suppliers=supplier, discount_percentage=37).exists()

    def test_update_supplier_discounts(self, authenticated_client: APIClient, supplier,
                                       supplier_discount) -> None:
        """Test updating a supplier's discount."""
        discount = supplier_discount
        supplier = supplier
        url = reverse('suppliers:supplier-update-discounts', kwargs={'pk': supplier.pk})
        start_date = datetime.now().replace(microsecond=0, tzinfo=None).isoformat()
        end_date = (datetime.now() + timezone.timedelta(days=7)).replace(microsecond=0, tzinfo=None).isoformat()

        updated_discount_data = {
            'id': discount.pk,
            'start_date': str(start_date) + 'Z',
            'end_date': str(end_date) + 'Z',
            'discount_percentage': 28.0,
            'is_active': True
        }

        response = authenticated_client.put(url, data=updated_discount_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        actual_data = json.loads(response.content)
        actual_data.pop('updated_at', None)
        actual_data.pop('created_at', None)
        assert actual_data == updated_discount_data
