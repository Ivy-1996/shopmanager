# Generated by Django 3.2.4 on 2021-06-08 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='店铺名称')),
                ('owner_name', models.CharField(max_length=50, verbose_name='店主姓名')),
                ('phone', models.CharField(max_length=20, verbose_name='店主电话')),
                ('shop_addr', models.CharField(max_length=50, verbose_name='店铺地址')),
                ('latitude', models.FloatField(verbose_name='纬度')),
                ('longitude', models.FloatField(verbose_name='经度')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('count', models.IntegerField(verbose_name='数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='价格')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update', models.DateTimeField(auto_now=True)),
                ('is_settle', models.BooleanField(default=False, verbose_name='是否结清')),
                ('remark', models.TextField(verbose_name='备注')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
            ],
        ),
    ]
