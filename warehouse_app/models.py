from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models import Min
from pathlib import PurePath


User = get_user_model()


def get_directory_path(instance, filename):
    return PurePath(f'{instance.city}', f'{filename}')


class Warehouse(models.Model):
    city = models.CharField(
        'Город',
        max_length=30
    )
    address = models.CharField(
        'Адрес',
        max_length=60
    )

    # странные поля этой модели (которые ниже), добавил потому что они в вёрстке есть, как нам с ними жить - не знаю :)

    description = models.CharField(
        'Описание',
        max_length=250,
        blank=True
    )
    contacts = models.CharField(
        'Контакты',
        max_length=150,
        blank=True
    )
    temperature = models.IntegerField(
        'Температура на складе',
        blank=True,
        null=True
    )
    ceiling_height = models.DecimalField(
        'Высота потолка',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True
    )
    image = models.ImageField(
        'Фото склада',
        upload_to=get_directory_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Склад города {self.city} {self.id}'

    @property
    def minimum_price(self):
        min_price = self.boxes.aggregate(min_price=Min('price'))['min_price']
        return min_price if min_price else 0

    @property
    def free_boxes_count(self):
        free_boxes = self.boxes.filter(is_busy=False).count()
        return free_boxes

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Box(models.Model):
    name = models.CharField(
        'Имя бокса',
        max_length=10,
    )
    size_choices = (
        ('LT3', 'До 3 м²'),
        ('LT10', 'До 10 м²'),
        ('GT10', 'От 10 м²')
    )
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name='Склад',
        related_name='boxes',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2
    )
    size = models.CharField(
        'Размер бокса',
        max_length=4,
        choices=size_choices
    )
    is_busy = models.BooleanField(
        'Занят ли бокс',
        default=False
    )

    def __str__(self):
        return f'{self.name}, {self.get_size_display()}, {self.warehouse}'

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name='Заказчик',
        related_name='orders',
        on_delete=models.CASCADE
    )
    box = models.ForeignKey(
        Box,
        verbose_name='Бокс',
        related_name='orders',
        on_delete=models.CASCADE
    )
    date_start = models.DateField(
        'Дата начала аренды',
        auto_now_add=True
    )
    date_end = models.DateField(
        'Дата конца аренды',
    )

    def __str__(self):
        return f'Заказ на {self.box} от {self.customer}'

    @property
    def expiration_time(self):
        today = now().date()
        delta = self.date_end - today
        return delta

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Stuff(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=40,
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='stuffs',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Заказ {self.order}'

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'