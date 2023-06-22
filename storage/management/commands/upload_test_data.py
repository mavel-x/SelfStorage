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
)


def create_user():
    users = (
        ('Светлана', '79998887701', 'user1@test.ru', 'Pa$$worD_1'),
        ('Екатерина', '79998887702', 'user2@test.ru', 'Pa$$worD_2'),
        ('Олег', '7999888703', 'user3@test.ru', 'Pa$$worD_3'),
        ('Пётр', '79998887704', 'user4@test.ru', 'Pa$$worD_4'),
        ('Наталья', '79998887705', 'user5@test.ru', 'Pa$$worD_5')
    )

    for user_notes in users:
        name, phone, email, password = user_notes
        user_obj, created = User.objects.get_or_create(
            email=email
        )

        if created:
            user_obj.phone = phone
            user_obj.username = name
            user_obj.password = password
            user_obj.save()

            print('\033[92mДобавлен пользователь:\033[0m', user_obj)
        else:
            print(f'\033[93mДублирование:\033[0m', user_obj.email)


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
        storage_obj, created = Storage.objects.get_or_create(
            address=address,
        )

        if created:
            storage_obj.city = city
            storage_obj.temp = random.choice(temperatures)
            storage_obj.height = round(random.uniform(2.5, 4.0), 1)
            storage_obj.save()

            print('\033[92mДобавлен склад:\033[0m', storage_obj)
        else:
            print(f'\033[93mДублирование:\033[0m', storage_obj)


def create_boxes():
    count_numbers = (180, 240, 300, 390)
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

            print(f'\033[92mДобавленs боксы:\033[0m {storage} - {storage.boxes.count()} шт.')

        else:
            print(f'\033[93mДублирование:\033[0m {storage} - {storage.boxes.count()} шт.')


def main():
    create_user()
    create_storages()
    create_boxes()


class Command(BaseCommand):
    help = 'Start adding test data'

    def handle(self, *args, **options):
        main()