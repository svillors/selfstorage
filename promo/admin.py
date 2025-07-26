from django.contrib import admin
from promo.models import TrackedLink, Promo


@admin.register(TrackedLink)
class TrackedLinkAdmin(admin.ModelAdmin):
    list_display = ['slug', 'target_url', 'clicks']
    readonly_fields = ['clicks']


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount']
