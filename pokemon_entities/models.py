from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, default='', verbose_name='Описание')
    title_en = models.CharField(blank=True, default='', max_length=200, verbose_name='Название на английском')
    title_jp = models.CharField(blank=True,  default='', max_length=200, verbose_name='Название на японском')
    previous_evolution = models.ForeignKey(
            "self",
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='next_evolutions',
            verbose_name='Из кого эволюционирует'
        )

    def __str__(self):
        return self.title


class  PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='entities', on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Появился')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Исчез')
    level = models.IntegerField(blank=True, null=True, verbose_name='Уровень')
    health = models.IntegerField(blank=True,null=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, null=True, verbose_name='Сила')
    defense = models.IntegerField(blank=True, null=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, verbose_name='Выносливость')
