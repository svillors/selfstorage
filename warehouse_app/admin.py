from django.contrib import admin
from warehouse_app.models import Warehouse, Box, Order, Stuff, Courier, Profile


class BoxesInline(admin.TabularInline):
    model = Box
    extra = 0
    fields = ['name', 'price', 'length', 'width', 'height', 'floor', 'is_busy']


class StuffInline(admin.TabularInline):
    model = Stuff
    extra = 0
    fields = ['name']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['city', 'address', 'free_boxes_count_display']
    inlines = [BoxesInline]

    def free_boxes_count_display(self, obj):
        return obj.free_boxes_count
    free_boxes_count_display.short_description = "Свободных боксов"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [StuffInline]
    list_display = ['box', 'date_start', 'date_end']
    readonly_fields = ('qr_code',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for box in Box.objects.prefetch_related('orders').all():
            if not box.orders.all().exists():
                box.is_busy = False
                box.save(update_fields=['is_busy'])
            else:
                box.is_busy = True
                box.save(update_fields=['is_busy'])


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'size', 'box_size', 'is_busy']


@admin.register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ['name','phone']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
