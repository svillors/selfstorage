from django.db import models


class TrackedLink(models.Model):
    slug = models.SlugField(
        'Идентификатор ссылки',
        unique=True
    )
    target_url = models.URLField(
        'Ссылка для редиректа'
    )
    clicks = models.PositiveIntegerField(
        'Количество переходов',
        default=0
    )

    def __str__(self):
        return f'{self.slug}, {self.target_url} - {self.clicks}'

    class Meta:
        verbose_name = 'Отслеживаемая ссылка'
        verbose_name_plural = 'Отслеживаемые ссылки'


class Promo(models.Model):
    code = models.CharField(
        'Промокод',
        max_length=10,
    )
    discount = models.PositiveSmallIntegerField(
        'Размер скидки'
    )

    def __str__(self):
        return f'{self.code}, {self.discount}'

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
