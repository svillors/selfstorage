from django.contrib import admin
from warehouse_app.models import Warehouse, Box, Order, Stuff


class BoxesInline(admin.TabularInline):
    model = Box
    extra = 0
    fields = ['name', 'size', 'price', 'is_busy']


class StuffInline(admin.TabularInline):
    model = Stuff
    extra = 0
    fields = ['name']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['city', 'address', 'free_boxes_count_display']
    inlines = [BoxesInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for box in obj.boxes.all():
            if box.orders.exists():
                box.is_busy = True
                box.save(update_fields=['is_busy'])

    def free_boxes_count_display(self, obj):
        return obj.free_boxes_count
    free_boxes_count_display.short_description = "Свободных боксов"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [StuffInline]
    list_display = ['box', 'date_start', 'date_end']


@admin.register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ['name']