import random
from datetime import datetime
import json
from rest_framework.authtoken.admin import User

from autosalons.models import  Specification, ShowroomHistory, ShowroomDiscount
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from autosalons.models import Showroom, Car, ShowroomCarRelationship
from autosalons.serializers import CarSerializer, ShowroomHistorySerializer, ShowroomDiscountSerializer, \
    SpecificationSerializer
from customers.models import Customer
from django.utils import timezone

from suppliers.models import Supplier

@pytest.fixture
def create_specification() -> Specification:
    specification = Specification.objects.create(name_of_car='Default Specification', color='красный', mileage=20000)
    return specification


@pytest.fixture
def create_discounts() -> ShowroomDiscount:
    start_date = timezone.now()
    end_date = start_date + timezone.timedelta(days=7)
    discount_percentage = 10

    discount_showroom = ShowroomDiscount.objects.create(start_date=start_date, end_date=end_date,
                                                        discount_percentage=discount_percentage)
    return discount_showroom


@pytest.fixture
def create_car(create_specification: Specification) -> Car:
    specification = create_specification
    serial_number = str(random.randint(100000, 999999))
    car = Car.objects.create(specification=specification, serial_number=serial_number)
    return car


@pytest.fixture
def create_showroom(create_car: Car, create_discounts: ShowroomDiscount) -> Showroom:
    car = create_car
    discount = create_discounts
    showroom = Showroom.objects.create(name='Test Showroom', location='Germany', balance=120000)
    showroom.discount_showroom.set([discount])
    return showroom


@pytest.fixture
def authenticated_client() -> APIClient:
    client = APIClient()
    return client


@pytest.fixture
def create_customer() -> Customer:
    user = User.objects.create(username='testuser')
    customer = Customer.objects.create(user=user, balance=0)
    return customer


@pytest.fixture
def create_showroom_history(create_showroom: Showroom, create_customer: Customer,
                            create_specification: Specification) -> Showroom:
    showroom = create_showroom
    car_1 = Car.objects.create(specification=create_specification, serial_number='1234673')
    car_2 = Car.objects.create(specification=create_specification, serial_number='6765489')

    customer = create_customer
    showroom_history_1 = ShowroomHistory.objects.create(
        car=car_1,
        amount=5,
        showroom=showroom,
        unique_customer=customer
    )
    showroom_history_2 = ShowroomHistory.objects.create(
        car=car_2,
        amount=7,
        showroom=showroom,
        unique_customer=customer
    )
    showroom.showroom_histories.add(showroom_history_1, showroom_history_2)

    return showroom


@pytest.fixture
def create_showroom_with_specifications(create_showroom: Showroom) -> Showroom:
    showroom = create_showroom

    spec_1 = Specification.objects.create(name_of_car='Spec 1', color='Red', mileage=5000)
    spec_2 = Specification.objects.create(name_of_car='Spec 2', color='Blue', mileage=8000)
    showroom.specifications.add(spec_1, spec_2)

    return showroom


@pytest.fixture
def create_showroom_with_different_cars(create_showroom: Showroom, create_specification: Specification) -> Showroom:
    showroom = create_showroom

    car_1 = Car.objects.create(specification=create_specification, serial_number='12345')
    car_2 = Car.objects.create(specification=create_specification, serial_number='67890')

    ShowroomCarRelationship.objects.create(showroom=showroom, car=car_1, price=5000, quantity=1)
    ShowroomCarRelationship.objects.create(showroom=showroom, car=car_2, price=7000, quantity=2)

    return showroom


@pytest.fixture
def create_showroom_with_discounts() -> Showroom:
    showroom = Showroom.objects.create(name='Test Showroom', location='Russia', balance=120000)

    discounts = [
        ShowroomDiscount.objects.create(start_date='2023-11-15', end_date='2023-12-15', discount_percentage=10.0),
        ShowroomDiscount.objects.create(start_date='2023-11-20', end_date='2023-12-20', discount_percentage=15.0)
    ]

    showroom.discount_showroom.set(discounts)
    return showroom


@pytest.fixture
def create_supplier() -> Supplier:
    return Supplier.objects.create(name='Тестовый поставщик', year_founded=2002)


@pytest.mark.django_db
class TestShowroomViews:

    def test_showroom_cars_action(self, authenticated_client: APIClient,
                                  create_showroom_with_different_cars: Showroom) -> None:
        """Test the action of retrieving cars in a showroom."""
        showroom = create_showroom_with_different_cars
        url = reverse('autosalons:showroom-cars', kwargs={'pk': showroom.id})
        response = authenticated_client.get(url)
        car_list = list(showroom.car.all())
        serializer = CarSerializer(car_list, many=True)
        expected_data = serializer.data
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_add_car(self, authenticated_client: APIClient, create_showroom: Showroom, create_car: Car) -> None:
        """Test the addition of a car to a showroom."""
        showroom = create_showroom
        car = create_car
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

    def test_showroom_history_action(self, authenticated_client: APIClient, create_showroom_history: Showroom) -> None:
        """Test the action of retrieving showroom history."""
        showroom = create_showroom_history
        url = reverse('autosalons:showroom-history', kwargs={'pk': showroom.id})
        response = authenticated_client.get(url)
        history_list = list(showroom.showroom_histories.all())
        serializer = ShowroomHistorySerializer(history_list, many=True)
        expected_data = serializer.data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_create_showroom_history(self, authenticated_client: APIClient, create_showroom: Showroom,
                                     create_customer: Customer, create_car: Car) -> None:
        """Test the creation of showroom history."""
        showroom = create_showroom
        customer = create_customer
        car = create_car
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
                                create_showroom_with_discounts: Showroom) -> None:
        """Test the action of retrieving showroom discounts."""
        showroom = create_showroom_with_discounts
        url = reverse('autosalons:showroom-discounts', kwargs={'pk': showroom.id})
        response = authenticated_client.get(url)

        discounts = ShowroomDiscount.objects.filter(showrooms_discount=showroom)
        serializer = ShowroomDiscountSerializer(discounts, many=True)
        expected_data = serializer.data
        assert response.data == expected_data
        assert response.status_code == status.HTTP_200_OK

    def test_create_discount(self, authenticated_client: APIClient, create_showroom: Showroom) -> None:
        """Test the creation of a discount for a showroom."""
        showroom = create_showroom
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

    def test_update_discounts(self, authenticated_client: APIClient, create_showroom: Showroom,
                              create_discounts: ShowroomDiscount) -> None:
        """Test the update of discounts for a showroom."""
        showroom = create_showroom
        discount_showroom = create_discounts

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
                                            create_showroom_with_specifications: Showroom) -> None:
        """Test the action of retrieving showroom specifications."""
        showroom = create_showroom_with_specifications
        url = reverse('autosalons:showroom-specifications', kwargs={'pk': showroom.id})
        response = authenticated_client.get(url)

        specifications = list(showroom.specifications.all())
        expected_data = SpecificationSerializer(specifications, many=True).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    # def test_add_specification_to_showroom(self, authenticated_client: APIClient, create_supplier: Supplier,
    #                                        create_showroom: Showroom) -> None:
    #     """Test adding a specification to a showroom."""
    #     showroom = create_showroom
    #     url = reverse('autosalons:showroom-add-specification', kwargs={'pk': showroom.id})
    #
    #     supplier = create_supplier
    #
    #     new_spec_data = {
    #         'name_of_car': 'New Car',
    #         'color': 'Red',
    #         'mileage': 1000,
    #         'supplier': supplier
    #     }
    #     response = authenticated_client.post(url, data=new_spec_data, format='json')
    #
    #     if response.status_code != status.HTTP_201_CREATED:
    #         print(f"Error creating specification: {response.content}")
    #
    #     assert Specification.objects.filter(name_of_car='New Car', color='Red', mileage=1000).exists()
