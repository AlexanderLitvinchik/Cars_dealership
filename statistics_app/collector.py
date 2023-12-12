from django.db.models import Sum, Max, Count
from autosalons.models import Showroom, ShowroomCarRelationship, ShowroomHistory, SupplierSpecificationRelationship
from customers.models import Customer
from suppliers.models import SupplierHistory, Supplier


def get_showroom_stat(showroom: Showroom):
    """
    Get statistics for a showroom.

    Parameters:
    - showroom (Showroom)

    Returns:
    - serializer data for showroom
    """
    cars_quantity_sold = ShowroomHistory.objects.filter(showroom=showroom).count() or 0
    money_earned = ShowroomHistory.objects.filter(showroom=showroom).aggregate(Sum('amount'))['amount__sum'] or 0
    money_spent = SupplierHistory.objects.filter(showroom=showroom).aggregate(Sum('amount'))['amount__sum'] or 0
    money_income = (money_earned or 0) - (money_spent or 0)
    most_expensive_deal = ShowroomHistory.objects.filter(showroom=showroom).aggregate(Max('amount'))[
                              'amount__max'] or 0

    top_cars = ShowroomHistory.objects.filter(showroom=showroom).values(
        'car__specification__name_of_car').annotate(
        total_sold=Count('car')).order_by('-total_sold')[:5]

    top_customers = ShowroomHistory.objects.filter(showroom=showroom).values('unique_customer').annotate(
        total_spent=Sum('amount')).order_by('-total_spent')[:5]

    top_suppliers = SupplierHistory.objects.filter(showroom=showroom).values(
        'supplier__name').annotate(
        total_purchased=Count('supplier')).order_by('-total_purchased')[:5]

    showroom_stat = {
        'showroom_name': showroom.name,
        'cars_quantity_sold': cars_quantity_sold,
        'money_earned': money_earned,
        'money_spent': money_spent,
        'money_income': money_income,
        'most_expensive_deal': most_expensive_deal,
        'top_cars': top_cars,
        'top_customers': top_customers,
        'top_suppliers': top_suppliers
    }
    return showroom_stat


def get_supplier_stat(supplier: Supplier):
    """
    Get statistics for a supplier.

    Parameters:
    - supplier (Supplier)

    Returns:
    - serializer data for supplier
    """
    cars_quantity_sold = SupplierHistory.objects.filter(supplier=supplier).count() or 0
    money_earned = SupplierHistory.objects.filter(supplier=supplier).aggregate(Sum('amount'))['amount__sum'] or 0

    most_expensive_deal = SupplierHistory.objects.filter(supplier=supplier).aggregate(Max('amount'))[
                              'amount__max'] or 0

    top_showrooms = SupplierHistory.objects.filter(supplier=supplier).values('showroom__name').annotate(
        total_purchased=Count('showroom')).order_by('-total_purchased')[:5]

    top_cars = SupplierHistory.objects.filter(supplier=supplier).values(
        'car__specification__name_of_car').annotate(
        total_sold=Count('car')).order_by('-total_sold')[:5]

    showroom_stat = {
        'supplier_name': supplier.name,
        'cars_quantity_sold': cars_quantity_sold,
        'money_earned': money_earned,
        'most_expensive_deal': most_expensive_deal,
        'top_showrooms': top_showrooms,
        'top_cars': top_cars,
    }
    return showroom_stat


def get_customer_stat(customer: Customer):
    """
    Get statistics for a customer.

    Parameters:
    - customer (Customer)

    Returns:
    - serializer data for customer
    """
    car_models_bought = ShowroomHistory.objects.filter(unique_customer=customer).values(
        'car__specification__name_of_car').distinct()

    cars_quantity = ShowroomHistory.objects.filter(unique_customer=customer).count()

    money_spent = ShowroomHistory.objects.filter(unique_customer=customer).aggregate(Sum('amount'))['amount__sum']

    data = {
        'customer_name': customer.user.username,
        'car_models_bought': car_models_bought,
        'cars_quantity': cars_quantity,
        'money_spent': money_spent,
    }
    return data
