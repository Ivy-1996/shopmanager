from django.db import models
from django_redis import get_redis_connection
from django.contrib.auth.models import User


# Create your models here.


class Shop(models.Model):
    REDIS_KEY = "shop:location"

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, verbose_name='店铺名称', help_text='店铺名称')
    owner_name = models.CharField(max_length=50, verbose_name='店主姓名', help_text='店主姓名')
    phone = models.CharField(max_length=20, verbose_name='店主电话', help_text='店主电话')
    shop_addr = models.CharField(max_length=50, verbose_name='店铺地址', help_text='店铺地址')
    latitude = models.FloatField(verbose_name='纬度', help_text='纬度')
    longitude = models.FloatField(verbose_name='经度', help_text='经度')

    def add_location_to_redis(self):
        coon = get_redis_connection('default')
        coon.geoadd(self.REDIS_KEY, self.longitude, self.latitude, self.pk)

    @classmethod
    def get_queryset_by_location(cls, queryset, longitude, latitude, radius):
        coon = get_redis_connection('default')
        result = coon.georadius(cls.REDIS_KEY, longitude, latitude, radius, unit='m')
        result = [int(i) for i in result]
        queryset = queryset.filter(id__in=result)
        return queryset

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '店铺'


class Goods(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='店铺')
    name = models.CharField(max_length=50, verbose_name='商品名称', help_text='商品名称')
    count = models.IntegerField(verbose_name='数量', help_text='商品数量')
    price = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='价格', help_text='商品价格')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update = models.DateTimeField(auto_now=True)
    is_settle = models.BooleanField(default=False, verbose_name='是否结清', help_text='是否结清')
    remark = models.TextField(verbose_name='备注', help_text='备注')

    class Meta:
        verbose_name = verbose_name_plural = '商品'

    def __str__(self):
        return self.name
