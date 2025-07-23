from django.contrib import admin
from promo.models import TrackedLink


@admin.register(TrackedLink)
class TrackedLinkAdmin(admin.ModelAdmin):
    list_display = ['slug', 'target_url', 'clicks']
    readonly_fields = ['clicks']
