from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField('Телефон', null=True, blank=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        blank=True,
        null=True,
        upload_to='images/avatars',
        validators=[FileExtensionValidator(
            ['jpg', 'jpeg', 'png',  'svg', 'webp']),
        ],
    )

    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return ' '.join((self.first_name, self.last_name))
        if name := (self.first_name or self.last_name):
            return name
        if self.username:
            return self.username
        return self.email


@receiver(pre_delete, sender=User)
def delete_photo(sender, instance, **kwargs):
    instance.avatar.delete()
