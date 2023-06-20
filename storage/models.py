from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from account.models import User


class Storage(models.Model):
    address = models.CharField('Адрес', max_length=200)
    temp = models.IntegerField('Температура (°С)')
    height = models.DecimalField(
        'Высота потолка (м)',
        max_digits=3,
        decimal_places=1,
    )
    price = models.DecimalField(
        'Цена за месяц',
        max_digits=9,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.address
    
    def first_image(self):
        return self.images.first()
    

class Image(models.Model):
    storage = models.ForeignKey(Storage,
                                on_delete=models.CASCADE,
                                related_name='images',
                                verbose_name='Склад')
    image = models.ImageField('Изображение')
    order = models.PositiveIntegerField('Порядок сортировки', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


@receiver(pre_delete, sender=Image)
def delete_image(sender, instance, **kwargs):
    instance.image.delete()


class Box(models.Model):
    number = models.IntegerField('Номер')
    storage = models.ForeignKey(
        Storage,
        on_delete=models.PROTECT,
        related_name='boxes',
        verbose_name='Склад',
    )

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'Бокс {self.number} {self.storage}'


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='Пользователь',
    )
    box = models.ForeignKey(
        Box,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='Бокс',
    )
    start_date = models.DateField('Дата начала аренды')
    end_date = models.DateField('Дата окончания аренды')

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def __str__(self):
        return f'{self.box} {self.start_date} - {self.end_date}'
