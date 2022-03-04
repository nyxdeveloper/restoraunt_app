# Generated by Django 3.2 on 2022-03-03 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import menu.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('img', models.ImageField(default=None, null=True, upload_to=menu.models.dish_img_path, verbose_name='Изображение')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('cost', models.DecimalField(decimal_places=2, default=1, max_digits=9)),
                ('proteins', models.FloatField(blank=True, default=0.0, verbose_name='Белки')),
                ('fats', models.FloatField(blank=True, default=0.0, verbose_name='Жиры')),
                ('carbohydrates', models.FloatField(blank=True, default=0.0, verbose_name='Углеводы')),
                ('cost_aggregated', models.BooleanField(default=False, verbose_name='Стоимость составляется из компонентов')),
                ('dishes', models.ManyToManyField(blank=True, to='menu.Dish', verbose_name='Входящие блюда')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
                'ordering': ['kind__name'],
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('img', models.ImageField(default=None, null=True, upload_to=menu.models.menu_img_path, verbose_name='Изображение')),
                ('weight', models.IntegerField(default=1, verbose_name='Позиция на экране')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True)),
                ('comment', models.TextField(blank=True, verbose_name='Коментарий')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('status', models.CharField(choices=[('in_process', 'Обрабатывается'), ('canceled', 'Отменен'), ('preparing', 'Готовится'), ('delivering', 'Доставляется'), ('is_deliver', 'Доставлен'), ('completed', 'Завершен')], default='in_process', max_length=20)),
                ('type', models.CharField(choices=[('delivery', 'Доставка'), ('pickup', 'Самовывоз'), ('on_spot', 'На месте')], default='on_spot', max_length=20)),
                ('address', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.address')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ToppingKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Вид допинга',
                'verbose_name_plural': 'Виды допингов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('img', models.ImageField(default=None, null=True, upload_to=menu.models.topping_img_path, verbose_name='Изображение')),
                ('cost', models.DecimalField(decimal_places=2, default=1, max_digits=9)),
                ('proteins', models.FloatField(blank=True, default=0.0, verbose_name='Белки')),
                ('fats', models.FloatField(blank=True, default=0.0, verbose_name='Жиры')),
                ('carbohydrates', models.FloatField(blank=True, default=0.0, verbose_name='Углеводы')),
                ('kind', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topings', to='menu.toppingkind', verbose_name='Вид')),
            ],
            options={
                'verbose_name': 'Допинг',
                'verbose_name_plural': 'Допинги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OrderPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1)),
                ('dish', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.dish')),
                ('dishes', models.ManyToManyField(related_name='complected', to='menu.Dish', verbose_name='Блюда')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='menu.order')),
            ],
            options={
                'verbose_name': 'Позиция заказа',
                'verbose_name_plural': 'Позиции заказов',
                'ordering': ['dish__name'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='toppings',
            field=models.ManyToManyField(to='menu.Topping', verbose_name='Допинги'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DishKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('menu', models.ManyToManyField(blank=True, related_name='dish_kinds', to='menu.Menu')),
            ],
            options={
                'verbose_name': 'Вид блюда',
                'verbose_name_plural': 'Виды блюд',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='dish',
            name='kind',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dishes', to='menu.dishkind', verbose_name='Вид'),
        ),
        migrations.AddField(
            model_name='dish',
            name='menu',
            field=models.ManyToManyField(blank=True, related_name='dishes', to='menu.Menu', verbose_name='Меню'),
        ),
    ]