from django.contrib import admin
from django.utils.safestring import mark_safe

from storage.models import (
    Storage,
    Image,
    Box,
    Booking,
    Discount,
    Invoice,
)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = (
        'address',
        'preview',
    )
    list_per_page = 20
    readonly_fields = ('preview',)

    @admin.display(description='Превью склада')
    def preview(self, obj):
        if obj.images:
            return mark_safe(
                f'<img src="{obj.images.get(order=1).image.url}" style="max-height: 100px;">'
            )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'storage',
        'order',
        'preview',
    )
    list_per_page = 20
    readonly_fields = ('preview',)

    @admin.display(description='Превью изображения')
    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 100px;">'
        )


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'storage',
        'number',
        'price',
    )
    list_per_page = 20


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'box',
        'move_out',
    )
    list_per_page = 20


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'promocode',
        'percent',
    )
    list_per_page = 20


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'booking',
        'amount',
        'final_date',
        'payment_status',
    )
    list_per_page = 20
