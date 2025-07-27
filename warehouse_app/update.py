from datetime import date, timedelta
from django.conf import settings
from django.core.mail import send_mail
from warehouse_app.models import Order


def is_date_end():
    orders = Order.objects.select_related('customer').all()
    for order in orders:
        delta = order.date_end - date.today()
        if delta.days in [30, 14, 7, 3]:
            send_mail(
                'Напоминание',
                f'Добрый день, срок аренды подходит к концу. Осталось {delta.days} дней',
                settings.EMAIL_HOST_USER,
                [order.customer.email]
            )
        if delta.days == 0:
            send_mail(
                'Напоминание',
                f'Добрый день, срок аренды истек. '
                f'Ваши вещи будут храниться 180 дней (до '
                f'{(date.today() + timedelta(days=(180))).strftime("%d-%m-%Y") }) '
                f'по повышенному тарифу (+10% от текущего тарифа), '
                f'после чего в случае, если вы так и не заберете вещи, вы их потеряете',
                settings.EMAIL_HOST_USER,
                [order.customer.email]
            )
        if delta.days in [-30, -60, -90, -120, -150, -180]:
            send_mail(
                'Напоминание',
                f'Добрый день, напоминаем, что вы потеряете ваши вещи, '
                f'если не заберете их до '
                f'{(date.today() + timedelta(days=(180 - abs(delta.days)))).strftime("%d-%m-%Y")}',
                settings.EMAIL_HOST_USER,
                [order.customer.email]
            )
