import json
import random
from datetime import datetime
import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from autosalons.models import Showroom, Car, Specification
from suppliers.models import Supplier, SupplierDiscount, SupplierHistory
from suppliers.serializers import SupplierDiscountSerializer, SupplierHistorySerializer, SupplierSerializer


@pytest.fixture
def authenticated_client() -> APIClient():
    client = APIClient()
    return client


@pytest.fixture
def create_showroom() -> Showroom:
    return Showroom.objects.create(name='Test Showroom', location='Germany', balance=120000)


@pytest.fixture
def create_supplier_discount() -> SupplierDiscount:
    start_date = timezone.now()
    discount = SupplierDiscount.objects.create(
        start_date=start_date,
        end_date=start_date + timezone.timedelta(days=7),
        discount_percentage=10
    )
    return discount


@pytest.fixture
def create_supplier() -> Supplier:
    return Supplier.objects.create(name='Тестовый поставщик', year_founded=2002)


@pytest.fixture
def create_showroom() -> Showroom:
    showroom = Showroom.objects.create(name='Test Showroom', location='Germany', balance=120000)
    return showroom


@pytest.fixture
def create_specification() -> Specification:
    specification = Specification.objects.create(name_of_car='Default Specification', color='красный', mileage=20000)
    return specification


@pytest.fixture
def create_car(create_specification: Specification) -> Car:
    serial_number = str(random.randint(100000, 999999))
    car = Car.objects.create(specification=create_specification, serial_number=serial_number)
    return car


@pytest.fixture
def create_supplier_history(create_showroom: Showroom, create_supplier: Supplier,
                            create_specification: Specification) -> Supplier:
    showroom = create_showroom

    car_1 = Car.objects.create(specification=create_specification, serial_number='1211173')
    car_2 = Car.objects.create(specification=create_specification, serial_number='6711189')

    supplier = create_supplier
    supplier_history_1 = SupplierHistory.objects.create(car=car_1, amount=4, showroom=showroom, supplier=supplier)
    supplier_history_2 = SupplierHistory.objects.create(car=car_2, amount=13, showroom=showroom, supplier=supplier)
    supplier.histories.add(supplier_history_1, supplier_history_2)

    return supplier


@pytest.fixture
def create_supplier_with_discounts() -> Supplier:
    supplier = Supplier.objects.create(name='Test Supplier', year_founded=2002)

    discounts = [
        SupplierDiscount.objects.create(start_date='2023-11-15', end_date='2023-12-15', discount_percentage=10.0),
        SupplierDiscount.objects.create(start_date='2023-11-20', end_date='2023-12-20', discount_percentage=15.0)
    ]

    supplier.discount_suppliers.set(discounts)
    return supplier


@pytest.mark.django_db
class TestSupplierViewSet:

    def test_suppliers_action(self, authenticated_client: APIClient, create_supplier: Supplier) -> None:
        """Test the action of retrieving suppliers."""
        supplier = create_supplier
        url = reverse('suppliers:supplier-list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        serializer = SupplierSerializer(supplier)
        assert response.data[0] == serializer.data

    def test_add_supplier(self, authenticated_client: APIClient) -> None:
        """Test the addition of a new supplier."""
        url = reverse('suppliers:supplier-list')
        data = {
            'name': 'Тестовый поставщик',
            'year_founded': 2009,
        }
        json_data = json.dumps(data)
        response = authenticated_client.post(url, data=json_data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Supplier.objects.filter(name='Тестовый поставщик', year_founded=2009).exists()

    def test_update_supplier(self, authenticated_client: APIClient, create_supplier: Supplier) -> None:
        """Test updating a supplier's information."""
        supplier = create_supplier
        data = {
            'name': 'Тестовый обновленный поставщик',
            'year_founded': 2009,
        }
        url = reverse('suppliers:supplier-detail', kwargs={'pk': supplier.pk})
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert Supplier.objects.filter(name='Тестовый обновленный поставщик', year_founded=2009).exists()

    def test_delete_supplier(self, authenticated_client: APIClient, create_supplier: Supplier) -> None:
        """Test deleting a supplier."""
        supplier = create_supplier
        url = reverse('suppliers:supplier-detail', kwargs={'pk': supplier.pk})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            Supplier.objects.get(pk=supplier.pk)

    def test_supplier_history(self, authenticated_client: APIClient, create_supplier_history: Supplier) -> None:
        """Test the retrieval of a supplier's history."""
        supplier = create_supplier_history
        url = reverse('suppliers:supplier-history', kwargs={'pk': supplier.id})
        response = authenticated_client.get(url)
        history_list = list(supplier.histories.all())
        serializer = SupplierHistorySerializer(history_list, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_create_supplier_history(self, authenticated_client: APIClient, create_supplier: Supplier,
                                     create_showroom: Showroom, create_car: Car) -> None:
        """Test the creation of a supplier's history."""
        supplier = create_supplier
        showroom = create_showroom
        car = create_car
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
                                create_supplier_with_discounts: Supplier) -> None:
        """Test the retrieval of a supplier's discounts."""
        supplier = create_supplier_with_discounts
        url = reverse('suppliers:supplier-discounts', kwargs={'pk': supplier.id})
        response = authenticated_client.get(url)
        discounts = SupplierDiscount.objects.filter(discount_suppliers=supplier)
        serializer = SupplierDiscountSerializer(discounts, many=True)
        expected_data = serializer.data
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_create_supplier_discount(self, authenticated_client: APIClient, create_supplier: Supplier) -> None:
        """Test the creation of a discount for a supplier."""
        supplier = create_supplier
        url = reverse('suppliers:supplier-create-discount', kwargs={'pk': supplier.id})
        data = {
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'discount_percentage': 37
        }
        response = authenticated_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert SupplierDiscount.objects.filter(discount_suppliers=supplier, discount_percentage=37).exists()

    def test_update_supplier_discounts(self, authenticated_client: APIClient, create_supplier: Supplier,
                                       create_supplier_discount: SupplierDiscount) -> None:
        """Test updating a supplier's discount."""
        discount = create_supplier_discount
        supplier = create_supplier
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
        print(response.content)
        assert response.status_code == status.HTTP_200_OK
        actual_data = json.loads(response.content)
        actual_data.pop('updated_at', None)
        actual_data.pop('created_at', None)
        assert actual_data == updated_discount_data
