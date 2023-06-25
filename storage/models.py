from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    FileExtensionValidator,
)
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

from account.models import User


class Storage(models.Model):
    city = models.CharField(
        'Город',
        max_length=200,
    )
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
        validators=[MinValueValidator(2.5),MaxValueValidator(10.0)]
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return  f'{self.city} - {self.address}'
    
    def first_image(self):
        return self.images.first()
    
    def count_boxes(self):
        return Box.objects.filter(storage=self).count()

    def count_empty_boxes(self):
        return Box.objects.filter(storage=self, is_busy=False).count()

    def get_min_price(self):
        return Box.objects.filter(storage=self).order_by('price').first().price

    def get_max_height(self):
        return Box.objects.filter(storage=self).order_by('-height').first()
    

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
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name='boxes',
        verbose_name='Склад',
    )
    number = models.PositiveIntegerField(
        'Номер',
        default=1,
        validators=[MinValueValidator(1)],
    )
    price = models.PositiveSmallIntegerField('Стоимость (руб./мес.)')
    floor = models.PositiveSmallIntegerField(
        'Этаж',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    width = models.DecimalField(
        'Ширина(М)',
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(4.0)]
    )
    height = models.DecimalField(
        'Высота(М)',
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(4.0)]
    )
    depth = models.DecimalField(
        'Глубина(М)',
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(4.0)]
    )
    square = models.DecimalField(
        'Площадь (М²)',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(1.0), MaxValueValidator(16.0)]
    )
    is_busy = models.BooleanField(
        verbose_name='Занят',
        default=False,
    )

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'Склад {self.storage.pk}, бокс {self.number}'


class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(terminated=False)

    def past(self):
        return self.filter(terminated=True)


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
    start_date = models.DateField('Дата начала аренды', null=True)
    end_date = models.DateField('Дата окончания аренды', null=True, blank=True)
    terminated = models.BooleanField('вещи вывезены', default=False)

    objects = BookingQuerySet.as_manager()

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def __str__(self):
        return f'{self.user.display_name}, {self.box}'

    def paid_until(self):
        last_payment = Invoice.objects.filter(booking=self, paid=True).last()
        if last_payment:
            return last_payment.pays_until

    def expired(self):
        return self.paid_until() is None or self.paid_until() < timezone.now().date()

    def expires_soon(self):
        if paid_until := self.paid_until():
            till_expiration = paid_until - timezone.now().date()
            return timezone.timedelta(0) < till_expiration <= timezone.timedelta(days=7)

    def liquidate_on(self):
        if paid_until := self.paid_until():
            return paid_until + timezone.timedelta(weeks=26)
        else:
            return self.start_date + timezone.timedelta(weeks=26)


class Discount(models.Model):
    promocode = models.CharField(
        'Промокод',
        max_length=10,
    )
    percent = models.SmallIntegerField(
        'Скидка (%)',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    start_date = models.DateField('Дата начала действия', null=True)
    end_date = models.DateField('Дата окончания действия', null=True, blank=True)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'{self.promocode} - скидка {self.percent}%'


class Invoice(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name='Аренда',
    )
    pays_until = models.DateField('Оплата до')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Сумма',
        validators=[MinValueValidator(500)],
    )
    paid = models.BooleanField(
        verbose_name='Оплачен',
        default=False,
    )
    payment_url = models.URLField(
        'Ссылка на оплату',
        blank=True,
        null=True,
    )
    cancelled = models.BooleanField(
        verbose_name='Отменен',
        default=False,
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='invoices',
        verbose_name='Скидка',
    )

    class Meta:
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.booking.user.display_name}: {self.booking.box} до {self.pays_until}'


class Lead(models.Model):
    email = models.EmailField('Email')
    name = models.CharField(
        'Имя',
        max_length=50,
        blank=True,
        null=True,
    )
    date = models.DateField(
        'Дата обращения',
        default=timezone.now,
    )
    description = models.CharField(
        'Описание',
        max_length=200,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'

    def __str__(self):
        return f'{self.email} {self.date}'
