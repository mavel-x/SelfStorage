from django.contrib import admin
from django.utils.safestring import mark_safe

from storage.models import (
    Storage,
    Image,
    Box,
    Booking,
    Discount,
    Invoice,
    Lead,
)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = (
        'city',
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
        'square',
        'floor',
        'is_busy'
    )
    list_per_page = 20

    def save_formset(self, request, form, formset, change):
        if 'width' in form.changed_data or 'depth' in form.changed_data :
           print(form.changed_data)

        formset.save(commit=False)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'box',
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
        'pays_until',
        'paid',
    )
    list_per_page = 20


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'date',
    )
    list_per_page = 20