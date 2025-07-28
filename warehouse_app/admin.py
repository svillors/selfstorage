from django.contrib import admin
from datetime import date
from warehouse_app.models import Warehouse, Box, Order, Courier, Profile, CallbackRequest


class BoxesInline(admin.TabularInline):
    model = Box
    extra = 0
    fields = ['name', 'price', 'length', 'width', 'height', 'floor', 'is_busy']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['city', 'address', 'free_boxes_count_display']
    inlines = [BoxesInline]

    def free_boxes_count_display(self, obj):
        return obj.free_boxes_count
    free_boxes_count_display.short_description = "Свободных боксов"


class IsExpiredFilter(admin.SimpleListFilter):
    title = 'Просрочен'
    parameter_name = 'expired'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        today = date.today()
        if self.value() == 'yes':
            return queryset.filter(date_end__lt=today)
        if self.value() == 'no':
            return queryset.filter(date_end__gte=today)
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['box', 'date_start', 'date_end', 'is_expired_display']
    list_filter = ('date_end', IsExpiredFilter)
    search_fields = ('customer__username', 'box__name')
    readonly_fields = ('qr_code', 'date_start')
    fields = [
        'customer', 'box',
        'date_start', 'date_end',
        'address', 'items',
        'phone', 'comment',
        'promocode', 'qr_code'
    ]

    @admin.display(boolean=True, description='Просрочен')
    def is_expired_display(self, obj):
        return obj.is_expired

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for box in Box.objects.prefetch_related('orders').all():
            if not box.orders.all().exists():
                box.is_busy = False
                box.save(update_fields=['is_busy'])
            else:
                box.is_busy = True
                box.save(update_fields=['is_busy'])


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ['name','phone']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
