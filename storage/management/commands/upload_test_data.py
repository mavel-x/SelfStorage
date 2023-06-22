import datetime
import random


from django.core.management.base import BaseCommand

from account.models import User
from storage.models import (
    Storage,
    Image,
    Box,
    Booking,
    Discount,
    Invoice,
    Lead,
)


def create_user():
    users = (
        ('Светлана Просрочка(вещи остались)', '79998887701', 'user1@test.ru', 'Pa$$w0rD'),
        ('Екатерина Использует(платит помесячно)', '79998887702', 'user2@test.ru', 'Pa$$w0rD'),
        ('Олег Съезжает(вещи забрал)', '7999888703', 'user3@test.ru', 'Pa$$worD_3'),
        ('Пётр Использует(оплатил весь срок)', '79998887704', 'user4@test.ru', 'Pa$$w0rD'),
        ('Наталья Будущее(хочет арендовать)', '79998887705', 'user5@test.ru', 'Pa$$w0rD'),
        ('Илья Резерв()', '79998887706', 'user6@test.ru', 'Pa$$w0rD'),
        ('Антон Резерв()', '79998887707', 'user7@test.ru', 'Pa$$w0rD'),
        ('Надежда Резерв()', '79998887708', 'user8@test.ru', 'Pa$$w0rD'),
        ('Ирина Резерв()', '79998887709', 'user9@test.ru', 'Pa$$w0rD'),
    )

    for user_notes in users:
        name, phone, email, password = user_notes
        user_obj, created = User.objects.get_or_create(email=email)

        if created:
            user_obj.phone = phone
            user_obj.username = name
            user_obj.password = password
            user_obj.save()

            print('\033[92mДобавлен пользователь:\033[0m', user_obj, user_obj.email)
        else:
            print(f'\033[93mПользователь уже существует:\033[0m', user_obj, user_obj.email)


def create_storages():
    city = 'Санкт-Петербург'
    addresses = (
        'ул. Марата, 82',
        'Новгородская улица, 12Б',
        'Серебристый бульвар, 18к1',
        'Лахтинский проспект, 2к3',
        'проспект Ветеранов, 173к4',
    )
    temperatures = (16, 18, 20)

    for address in addresses:
        storage_obj, created = Storage.objects.get_or_create(address=address)

        if created:
            storage_obj.city = city
            storage_obj.temp = random.choice(temperatures)
            storage_obj.height = round(random.uniform(2.5, 4.0), 1)
            storage_obj.save()

            print('\033[92mДобавлен склад:\033[0m', storage_obj)
        else:
            print(f'\033[93mСклад уже существует:\033[0m', storage_obj)


def create_boxes():
    count_numbers = (30, 60, 90, 120)
    one_metr_amount = 1599
    floors = (1, 2, 3)
    sizes = (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0)

    for storage in Storage.objects.all():
        if not storage.boxes.all():
            count = random.choice(count_numbers)
            floor = random.choice(floors)

            for num in range(1, count+1, floor):
                width = random.choice(sizes)
                height = round(random.uniform(1.0, storage.height.__float__()), 1)
                depth = random.choice(sizes)
                square = width * depth
                price = square * one_metr_amount

                for floor_corrector in range(floor):
                    Box.objects.create(
                        storage=storage,
                        number=num + floor_corrector,
                        price=price,
                        floor=1 + floor_corrector,
                        width=width,
                        height=height,
                        depth=depth,
                        square=square,
                    )

            print(f'\033[92mДобавлены боксы:\033[0m {storage} - {storage.boxes.count()} штук боксов.')

        else:
            print(f'\033[93mСклад уже имеет боксы:\033[0m {storage} - {storage.boxes.count()} штук боксов.')


def create_bookings():
    bookings = (
        (
            User.objects.get(email='user1@test.ru'),
            '2023-01-01',
            '2023-04-01',
            True, # Бокс занят
        ),
        (
            User.objects.get(email='user2@test.ru'),
            '2023-01-01',
            '2023-05-01',
            True, # Бокс занят
        ),
        (
            User.objects.get(email='user3@test.ru'),
            '2023-01-01',
            '2023-07-01',
            False, # Бокс занят
        ),
        (
            User.objects.get(email='user4@test.ru'),
            '2023-01-01',
            '2024-01-01',
            True, # Бокс занят
        ),
        (
            User.objects.get(email='user5@test.ru'),
            datetime.datetime.today().date(),
            '2023-12-01',
            False, # Бокс занят
        ),
    )

    for booking_notes in bookings:
        print(booking_notes)

        user, start_date, end_date, is_busy = booking_notes
        booking_obj, created = Booking.objects.get_or_create(
            user=user,
            box=random.choice(Box.objects.filter(is_busy=False)),
        )

        print(booking_obj)

        if created:
            booking_obj.start_date = start_date
            booking_obj.end_date = end_date
            booking_obj.save()

            booking_obj.box.is_busy = is_busy
            booking_obj.box.save()

            print('\033[92mДобавлена аренда:\033[0m', user, booking_obj)
        else:
            print(f'\033[93mАренда уже существует:\033[0m', user, booking_obj)


def create_discounts():
    discounts = (
        ('SALE', 10, datetime.datetime.today().date(), '2023-08-31'),
        ('SPRING', 15, '2023-02-01', '2023-03-01'),
        ('SUMMER15', 15, '2023-05-01', '2023-07-01'),
        ('SUMMER20', 20, '2023-05-01', '2023-07-01'),
        ('AUTUMN', 10, '2023-08-01', '2023-09-01'),
        ('WINTER', 15, '2023-10-01', '2023-11-01'),
    )

    for lead_notes in discounts:
        promocode, percent, start_date, end_date = lead_notes
        lead_obj, created = Discount.objects.get_or_create(promocode=promocode)

        if created:
            lead_obj.percent = percent
            lead_obj.start_date = start_date
            lead_obj.end_date = end_date
            lead_obj.save()

            print('\033[92mДобавлена скидка:\033[0m', lead_obj)
        else:
            print(f'\033[93mСкидка уже существует:\033[0m', lead_obj)


def create_leads():
    leads = (
        ('Ольга', 'lead1@test.ru', datetime.datetime.today().date(), 'Хочу хранить мебель, важна влажность!'),
        ('Андрей', 'lead2@test.ru', '2023-01-10', 'Ищу места для хранения консервы!'),
        ('Виктор', 'lead3@test.ru', '2022-12-16', 'А у вас автомобиль можно припарковать?'),
        ('Семён', 'lead4@test.ru', '2023-06-10', ''),
        ('', 'lead5@test.ru', datetime.datetime.today().date(), ''),
    )

    for lead_notes in leads:
        name, email, date, description = lead_notes
        lead_obj, created = Lead.objects.get_or_create(email=email)

        if created:
            lead_obj.name = name
            lead_obj.date = date
            lead_obj.description = description
            lead_obj.save()

            print('\033[92mДобавлен лид:\033[0m', lead_obj)
        else:
            print(f'\033[93mЛид уже существует:\033[0m', lead_obj)


def main(**options):
    if options.get('d'):
        for model in (
            Invoice,
            Booking,
            Box,
            Storage,
            Image,
            Discount,
            User,
            Lead,
        ):
            print(f'Очистка модели {model.__name__}', end=' ')
            if model is User:
                model.objects.filter(is_staff=False).delete()
            else:
                model.objects.all().delete()
            print('- \033[92mDONE\033[0m.')

    create_user()
    create_storages()
    create_boxes()
    create_bookings()
    create_leads()
    create_discounts()


class Command(BaseCommand):
    help = 'Start adding test data'

    def handle(self, *args, **options):
        main(**options)

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            action='store_const',
            const=True,
        )
