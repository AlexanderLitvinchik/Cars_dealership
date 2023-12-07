import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from customers.models import Customer, User
from customers.serializers import CustomerSerializer
from rest_framework.test import APIClient
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
def customer():
    return G(Customer, user=G(User, username='testuser2'), balance=0)


"""
    Added fixtures for urls
"""


@pytest.fixture
def customers_list_url():
    return reverse('customers:customer-list')


@pytest.fixture
def customer_detail_url(customer):
    return reverse('customers:customer-detail', kwargs={'pk': customer.pk})


@pytest.mark.django_db
class TestCustomerViewSet:
    def test_customers_action(self, authenticated_client: APIClient, customer, customers_list_url) -> None:
        """Test the action of retrieving customers."""
        response = authenticated_client.get(customers_list_url)
        serializer = CustomerSerializer(customer)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [serializer.data]

    def test_add_customer(self, authenticated_client: APIClient, customers_list_url) -> None:
        """Test the addition of a new customer."""
        user = User.objects.create(username='testuser4')
        data = {
            'user': user.id,
            'balance': 1000.00,
        }
        response = authenticated_client.post(customers_list_url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.filter(balance=1000.00, user=user).exists()

    def test_update_customer(self, authenticated_client: APIClient, customer, customer_detail_url) -> None:
        """Test updating a customer's information."""
        user = customer.user
        user.username = 'testuser_updated'
        user.save()
        data = {
            'user': user.id,
            'balance': 2111.00,
        }
        response = authenticated_client.put(customer_detail_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert Customer.objects.filter(balance=2111.00, user=user).exists()

    def test_delete_customer(self, authenticated_client: APIClient, customer, customer_detail_url) -> None:
        """Test deleting a customer."""
        response = authenticated_client.delete(customer_detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Customer.objects.filter(pk=customer.pk).exists()
