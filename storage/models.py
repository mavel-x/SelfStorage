from dateutil import relativedelta
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from account.models import User


class Storage(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=200,
    )
    temp = models.SmallIntegerField(
        'Температура (°С)',
        default=20,
    )
    height = models.DecimalField(
        'Высота потолка (м)',
        max_digits=3,
        decimal_places=1,
        default=2.5,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.address
    
    def first_image(self):
        return self.images.first()
    

class Image(models.Model):
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Склад',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='images/storages',
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png',  'svg', 'webp']),
        ],
    )
    order = models.PositiveIntegerField(
        'Порядок сортировки',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


@receiver(pre_delete, sender=Image)
def delete_image(sender, instance, **kwargs):
    instance.image.delete()


class Box(models.Model):
    number = models.PositiveIntegerField(
        'Номер',
        default=1,
        validators=[MinValueValidator(1)],
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.PROTECT,
        related_name='boxes',
        verbose_name='Склад',
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Стоимость (руб./мес.)',
    )

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'{self.storage} - бокс №{self.number}'


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
    amount = models.PositiveSmallIntegerField(
        verbose_name='Стоимость аренды',
        validators=[MinValueValidator(500)],
    )
    payment_url = models.URLField(
        'Ссылка на оплату',
        blank=True,
        null=True,
    )
    payment_status = models.BooleanField(
        verbose_name='Оплачено',
        default=False,
    )

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def __str__(self):
        return f'{self.box} {self.start_date} - {self.end_date}'

    def save(self, *args, **kwargs):
        months_difference = relativedelta.relativedelta(self.end_date, self.start_date).months
        self.amount = self.box.price * months_difference

        super(Booking, self).save(*args, **kwargs)


class Discount(models.Model):
    storage = models.ManyToManyField(
        Storage,
        related_name='discounts',
        verbose_name='Склады',
    )
    promocode = models.CharField(
        'Промокод',
        max_length=10,
    )
    percent = models.SmallIntegerField(
        'Процентная скидка',
        default=0,
        validators=[MinValueValidator(0)],
    )
    money = models.SmallIntegerField(
        'Денежная скидка',
        default=0,
        validators=[MinValueValidator(0)],
    )
    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.promocode
