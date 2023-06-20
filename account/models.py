from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    phone = PhoneNumberField('Телефон')
    avatar = models.ImageField(
        verbose_name='Аватар',
        blank=True,
        null=True,
        upload_to='images/avatars',
        validators=[FileExtensionValidator(
            ['jpg', 'jpeg', 'png',  'svg', 'webp']),
        ],
    )


@receiver(pre_delete, sender=User)
def delete_photo(sender, instance, **kwargs):
    instance.avatar.delete()
