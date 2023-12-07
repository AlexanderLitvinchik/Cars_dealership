from datetime import timedelta, datetime
import random
from _decimal import Decimal
from celery import Task
from django.db import transaction
from django.db.models import Min, F, ExpressionWrapper, DecimalField, Case, When, Count
from autosalons.models import Showroom, SupplierSpecificationRelationship, Car, ShowroomCarRelationship, ShowroomHistory
from carsdealership.celery import app
from customers.models import Offer, Customer
from suppliers.models import Supplier, SupplierHistory
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


def get_sorted_specifications(showroom):
    # Сортируем спецификации по количеству проданных единиц в истории продаж
    specifications = showroom.specifications.annotate(
        total_sold=Count('car_specification__saled_cars')
    ).order_by('-total_sold')

    return specifications


def get_min_price_for_showroom(specification):
    return SupplierSpecificationRelationship.objects.filter(
        specification=specification,
        supplier__is_active=True,
    ).annotate(
        min_price=Case(
            When(discount_supplier__is_active=True, then=ExpressionWrapper(
                F('supplier_specification_price') * (
                        1 - F('discount_supplier__discount_percentage') / 100),
                output_field=DecimalField()
            )),
            default=F('supplier_specification_price'),
            output_field=DecimalField(),
        ),
    ).order_by('min_price', 'supplier_specification_price').first()


def get_min_price_for_customers(specification):
    return ShowroomCarRelationship.objects.filter(
        car__specification=specification,
        showroom__is_active=True,
    ).annotate(
        min_price=Case(
            When(showroom__discount_showroom__is_active=True,
                 then=F('price') * (1 - F('showroom__discount_showroom__discount_percentage') / 100)),
            default=F('price'),
            output_field=DecimalField(),
        ),
    ).order_by('min_price').first()


class ShowroomsBuyingCarTask(Task):
    def run(self, *args, **kwargs):
        logger.info(f"Starting showrooms_buying_car")
        with transaction.atomic():
            for showroom in Showroom.objects.all():
                specifications = get_sorted_specifications(showroom)
                for specification in specifications.prefetch_related(
                        'suppliers_specification',
                        'suppliers_specification__supplier',
                        'suppliers_specification__discount_supplier'
                ).all():
                    min_price = get_min_price_for_showroom(specification)

                    if min_price is not None and showroom.balance >= min_price.min_price:
                        # скидка для потоянного покупателя проверяем можно ли ее примеерять
                        purchase_count = SupplierHistory.objects.filter(
                            supplier=min_price.supplier,
                            showroom=showroom
                        ).aggregate(total_purchases=Count('id'))['total_purchases']

                        # Уменьшаем цену для автосалона на 1 процент при 20 покупках, но больше 20% поулчить нельзя
                        discount_percentage = min(purchase_count // 20, 20)
                        discounted_price = min_price.min_price * Decimal((1 - discount_percentage / 100))
                        showroom.balance -= discounted_price
                        showroom.save()

                        # Проверяем наличие машин с той же спецификацией в текущем автосалоне
                        existing_cars = ShowroomCarRelationship.objects.filter(
                            showroom=showroom,
                            car__specification=specification
                        )

                        if existing_cars.exists():
                            # Если уже есть машины с такой спецификацией, увеличиваем количество
                            showroom_car = existing_cars.first()
                            showroom_car.quantity += 1
                            showroom_car.save()
                        else:
                            # Если нет машин с такой же спецификацией, создаем новый объект
                            car = Car.objects.create(specification=specification,
                                                     serial_number=str(random.randint(100000, 999999)))

                            ShowroomCarRelationship.objects.create(
                                car=car,
                                showroom=showroom,
                                price=min_price.min_price * Decimal('1.3'),
                                quantity=1
                            )

                        supplier = min_price.supplier
                        car_to_use = existing_cars.first().car if existing_cars.exists() else car
                        SupplierHistory.objects.create(
                            supplier=supplier,
                            showroom=showroom,
                            car=car_to_use,
                            amount=discounted_price
                        )


class UpdateSupplierShowroomTask(Task):
    def run(self, *args, **kwargs):
        for showroom in Showroom.objects.all():
            print(showroom.specifications.all())
            for specification in showroom.specifications.all():
                min_price = get_min_price_for_showroom(specification)
                if min_price is not None:
                    showroom.update_or_add_supplier(min_price.supplier)


class CustomersBuyingCarTask(Task):
    def run(self, *args, **kwargs):
        customers = Customer.objects.all()
        for customer in customers:
            active_offers = Offer.objects.filter(customer=customer)
            print(customer)
            for offer in active_offers:
                self.find_matching_showroom_car(offer)

    def find_matching_showroom_car(self, offer):
        # Поиск подходящего автомобиля по предложению
        matching_cars = ShowroomCarRelationship.objects.filter(
            car__specification__name_of_car=offer.name_of_car,
            car__specification__year=offer.year,
            quantity__gt=0
        ).annotate(
            discounted_price=Case(
                When(showroom__discount_showroom__is_active=True,
                     then=F('price') * (1 - F('showroom__discount_showroom__discount_percentage') / 100)),
                default=F('price'),
                output_field=DecimalField(),
            )
        ).order_by('discounted_price').first()

        if matching_cars:
            # Проверяем цену, и если она удовлетворяет вашим критериям, возвращаем автомобиль
            if matching_cars.discounted_price <= offer.max_price and matching_cars.discounted_price <= offer.customer.balance:
                # Уменьшаем баланс пользователя с учетом скидки
                customer = offer.customer
                customer.balance -= matching_cars.discounted_price
                customer.save()

                # Создаем запись в истории покупок
                ShowroomHistory.objects.create(
                    showroom=matching_cars.showroom,
                    car=matching_cars.car,
                    amount=matching_cars.discounted_price,
                    unique_customer=customer
                )
                return matching_cars.showroom, matching_cars, matching_cars.discounted_price
        return None


@app.task(base=ShowroomsBuyingCarTask)
def run_showrooms_buying_car_task():
    # breakpoint()
    task = ShowroomsBuyingCarTask()
    # breakpoint()
    task.run()


@app.task(base=CustomersBuyingCarTask)
def run_customers_buying_car_task():
    # breakpoint()
    task = CustomersBuyingCarTask()
    # breakpoint()
    task.run()


@app.task(base=UpdateSupplierShowroomTask)
def showrooms_update_suppliers():
    # breakpoint()
    task = UpdateSupplierShowroomTask()
    # breakpoint()
    task.run()
