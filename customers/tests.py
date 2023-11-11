import pytest
from rest_framework import status
from django.urls import reverse
from customers.models import Customer, User
from customers.serializers import CustomerSerializer
from rest_framework.test import APIClient


@pytest.fixture
def authenticated_client() -> APIClient:
    client = APIClient()
    return client


@pytest.fixture
def create_customer():
    user = User.objects.create(username='testuser')
    customer = Customer.objects.create(user=user, balance=0)
    return customer


@pytest.mark.django_db
class TestCustomerViewSet:
    def test_customers_action(self,authenticated_client: APIClient, create_customer: Customer) -> None:
        """Test the action of retrieving customers."""
        customer = create_customer
        url = reverse('customers:customer-list')
        response = authenticated_client.get(url)
        serializer = CustomerSerializer(customer)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0] == serializer.data

    def test_add_customer(self,authenticated_client: APIClient) -> None:
        """Test the addition of a new customer."""
        url = reverse('customers:customer-list')
        user = User.objects.create(username='testuser')
        data = {
            'user': user.id,
            'balance': 1000.00,
        }
        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.filter(balance=1000.00, user=user).exists()

    def test_update_customer(self,authenticated_client: APIClient, create_customer: Customer) -> None:
        """Test updating a customer's information."""
        customer = create_customer
        url = reverse('customers:customer-detail', kwargs={'pk': customer.pk})
        user = customer.user
        user.username = 'testuser_updated'
        user.save()

        data = {
            'user': user.id,
            'balance': 2111.00,
        }
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert Customer.objects.filter(balance=2111.00, user=user).exists()

    def test_delete_customer(self,authenticated_client: APIClient, create_customer: Customer) -> None:
        """Test deleting a customer."""
        customer = create_customer
        url = reverse('customers:customer-detail', kwargs={'pk': customer.pk})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Customer.objects.filter(pk=customer.pk).exists()
