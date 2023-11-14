import random
from datetime import datetime
import json
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

from autosalons.models import Specification, ShowroomHistory, ShowroomDiscount
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from autosalons.models import Showroom, Car, ShowroomCarRelationship
from autosalons.serializers import CarSerializer, ShowroomHistorySerializer, ShowroomDiscountSerializer, \
    SpecificationSerializer, ShowroomSerializer

from customers.tests import customer
from django.utils import timezone
from suppliers.models import Supplier
from ddf import G, F

from suppliers.serializers import SupplierSerializer


@pytest.fixture
def authenticated_user() -> User:
    user = G(User, username='testuser3')
    return user


@pytest.fixture
def authenticated_client(authenticated_user: User) -> APIClient:
    client = APIClient()
    access_token = AccessToken.for_user(authenticated_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


@pytest.fixture
def specification() -> Specification:
    return G(Specification, name_of_car='Default Specification', color='красный', mileage=20000)


@pytest.fixture
def discounts() -> ShowroomDiscount:
    return G(ShowroomDiscount, start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=7),
             discount_percentage=10)


@pytest.fixture
def car(specification: Specification) -> Car:
    return G(Car, specification=specification, serial_number=str(random.randint(100000, 999999)))


@pytest.fixture
def showroom(car: Car, discounts: ShowroomDiscount) -> Showroom:
    return G(Showroom, name='Test Showroom', location='Germany', balance=120000, discount_showroom=[discounts])


@pytest.fixture
def showroom_history(showroom: Showroom, customer, specification: Specification) -> Showroom:
    showroom.showroom_histories.add(
        G(ShowroomHistory, car=G(Car, specification=specification, serial_number='1234673'), amount=5,
          showroom=showroom, unique_customer=customer),
        G(ShowroomHistory, car=G(Car, specification=specification, serial_number='6765489'), amount=7,
          showroom=showroom, unique_customer=customer)
    )
    return showroom


@pytest.fixture
def showroom_specifications(showroom: Showroom, specification: Specification) -> Showroom:
    spec_1 = G(Specification, name_of_car='Spec 1', color='Red', mileage=5000)
    spec_2 = G(Specification, name_of_car='Spec 2', color='Blue', mileage=8000)
    showroom.specifications.set([spec_1, spec_2])
    return showroom


@pytest.fixture
def showroom_different_cars(showroom: Showroom, specification: Specification) -> Showroom:
    G(ShowroomCarRelationship, showroom=showroom, car=G(Car, specification=specification, serial_number='12345'),
      price=5000, quantity=1)
    G(ShowroomCarRelationship, showroom=showroom, car=G(Car, specification=specification, serial_number='67890'),
      price=7000, quantity=2)
    return showroom


@pytest.fixture
def showroom_discounts() -> Showroom:
    showroom = G(Showroom, name='Test Showroom', location='Russia', balance=120000)
    discounts = [
        G(ShowroomDiscount, start_date='2023-11-15', end_date='2023-12-15', discount_percentage=10.0),
        G(ShowroomDiscount, start_date='2023-11-20', end_date='2023-12-20', discount_percentage=15.0)
    ]
    showroom.discount_showroom.set(discounts)
    return showroom


@pytest.fixture
def supplier() -> Supplier:
    return G(Supplier, name='Тестовый поставщик', year_founded=2002)


"""
    Added fixtures for urls
"""


@pytest.fixture
def showrooms_list_url() -> str:
    return reverse('autosalons:showroom-list')


@pytest.fixture
def showroom_detail_url(showroom: Showroom) -> str:
    return reverse('autosalons:showroom-detail', kwargs={'pk': showroom.pk})


@pytest.mark.django_db
class TestShowroomViews:
    """Created tests of showroom"""

    def test_read_showroom(self, authenticated_client: APIClient, showrooms_list_url: str, showroom: Showroom) -> None:
        """Test reading a showroom."""
        response = authenticated_client.get(showrooms_list_url)
        serializer = ShowroomSerializer(showroom)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [serializer.data]

    def test_add_showroom(self, specification: Specification, showrooms_list_url: str,
                          authenticated_client: APIClient) -> None:
        """Test adding a new showroom."""
        data = {
            'name': 'Test Showroom',
            'location': 'AZ',
            'balance': 120000,
            'specifications': [SpecificationSerializer(specification).data]
        }
        json_data = json.dumps(data)
        response = authenticated_client.post(showrooms_list_url, data=json_data, content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Showroom.objects.filter(name='Test Showroom', location='AZ', balance=120000).exists()

    def test_update_showroom(self, specification: Specification, showroom_detail_url: str,
                             authenticated_client: APIClient) -> None:
        """Test updating an existing showroom."""
        updated_data = {
            'name': 'Updated Showroom',
            'location': 'AZ',
            'balance': 150000,
            'specifications': [SpecificationSerializer(specification).data]
        }

        response = authenticated_client.put(showroom_detail_url, data=json.dumps(updated_data),
                                            content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert Showroom.objects.filter(name='Updated Showroom', location='AZ', balance=150000).exists()

    def test_delete_showroom(self, showroom_detail_url: str, authenticated_client: APIClient,
                             showroom: Showroom) -> None:
        """Test deleting a showroom."""
        response = authenticated_client.delete(showroom_detail_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Showroom.objects.filter(pk=showroom.pk).exists()

    def test_showroom_cars_action(self, authenticated_client: APIClient,
                                  showroom_different_cars) -> None:
        """Test the action of retrieving cars in a showroom."""
        showroom = showroom_different_cars
        url = reverse('autosalons:showroom-cars', kwargs={'pk': showroom.id})
        response = authenticated_client.get(url)
        car_list = list(showroom.car.all())
        serializer = CarSerializer(car_list, many=True)
        expected_data = serializer.data
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_add_car(self, authenticated_client: APIClient, showroom, car) -> None:
        """Test the addition of a car to a showroom."""
        url = reverse('autosalons:showroom-add-car', kwargs={'pk': showroom.id})
        data = {
            'car': car.id,
            'price': 30000,
            'quantity': 5,
            'showroom': showroom.id
        }
        json_data = json.dumps(data)
        response = authenticated_client.post(url, data=json_data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        assert ShowroomCarRelationship.objects.filter(showroom=showroom, car=car, price=30000, quantity=5).exists()

    def test_showroom_history_action(self, authenticated_client: APIClient, showroom_history) -> None:
        """Test the action of retrieving showroom history."""
        showroom = showroom_history
        url = reverse('autosalons:showroom-history', kwargs={'pk': showroom.id})
        response = authenticated_client.get(url)
        history_list = list(showroom.showroom_histories.all())
        serializer = ShowroomHistorySerializer(history_list, many=True)
        expected_data = serializer.data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_create_showroom_history(self, authenticated_client: APIClient, showroom,
                                     customer, car) -> None:
        """Test the creation of showroom history."""
        url = reverse('autosalons:showroom-create-history', kwargs={'pk': showroom.id})
        data = {
            'car': car.id,
            'amount': 50000,
            'showroom': showroom.id,
            'unique_customer': customer.id
        }
        json_data = json.dumps(data)
        response = authenticated_client.post(url, data=json_data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        assert ShowroomHistory.objects.filter(
            showroom=showroom, amount=50000, unique_customer=customer, car=car
        ).exists()

    def test_showroom_discounts(self, authenticated_client: APIClient,
                                showroom_discounts) -> None:
        """Test the action of retrieving showroom discounts."""
        showroom = showroom_discounts
        url = reverse('autosalons:showroom-discounts', kwargs={'pk': showroom.id})
        response = authenticated_client.get(url)

        discounts = ShowroomDiscount.objects.filter(showrooms_discount=showroom)
        serializer = ShowroomDiscountSerializer(discounts, many=True)
        expected_data = serializer.data
        assert response.data == expected_data
        assert response.status_code == status.HTTP_200_OK

    def test_create_discount(self, authenticated_client: APIClient, showroom) -> None:
        """Test the creation of a discount for a showroom."""
        showroom = showroom
        url = reverse('autosalons:showroom-create-discount', kwargs={'pk': showroom.id})

        data = {
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'discount_percentage': 19
        }
        response = authenticated_client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert ShowroomDiscount.objects.filter(showrooms_discount=showroom,
                                               discount_percentage=19).exists()

    def test_update_discounts(self, authenticated_client: APIClient, showroom,
                              discounts) -> None:
        """Test the update of discounts for a showroom."""
        showroom = showroom
        discount_showroom = discounts

        url = reverse('autosalons:showroom-update-discounts', kwargs={'pk': showroom.pk})

        start_date = datetime.now().replace(microsecond=0, tzinfo=None).isoformat()
        end_date = (datetime.now() + timezone.timedelta(days=7)).replace(microsecond=0, tzinfo=None).isoformat()

        updated_discount_data = {
            'id': discount_showroom.pk,
            'start_date': str(start_date) + 'Z',
            'end_date': str(end_date) + 'Z',
            'discount_percentage': 23.0,
            'is_active': True
        }

        response = authenticated_client.put(url, data=updated_discount_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        actual_data = json.loads(response.content)
        actual_data.pop('updated_at', None)
        actual_data.pop('created_at', None)
        assert actual_data == updated_discount_data

    def test_showroom_specifications_action(self, authenticated_client: APIClient,
                                            showroom_specifications) -> None:
        """Test the action of retrieving showroom specifications."""
        showroom = showroom_specifications
        url = reverse('autosalons:showroom-specifications', kwargs={'pk': showroom.id})
        response = authenticated_client.get(url)

        specifications = list(showroom.specifications.all())
        expected_data = SpecificationSerializer(specifications, many=True).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_add_specification_to_showroom(self, authenticated_client: APIClient, supplier: Supplier,
                                           showroom: Showroom) -> None:
        """Test adding a specification to a showroom."""
        url = reverse('autosalons:showroom-add-specification', kwargs={'pk': showroom.id})
        new_spec_data = {
            'name_of_car': 'New Car',
            'color': 'Red',
            'mileage': 1000,
            'supplier': [SupplierSerializer(supplier).data]
        }
        response = authenticated_client.post(url, data=new_spec_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Specification.objects.filter(name_of_car='New Car', color='Red', mileage=1000).exists()
