from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.Shop)
class ShopModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'owner_name', 'phone', 'shop_addr', 'latitude', 'longitude']
    list_filter = ['user', 'name', 'shop_addr']


@admin.register(models.Goods)
class GoodsModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'name', 'count', 'price', 'total', 'create_time', 'is_settle', 'remark']

    list_filter = ['name', 'is_settle']

    def total(self, row):
        return row.count * row.price

    total.short_description = '总价'

    def get_queryset(self, request):
        queryset = super(GoodsModelAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(shop__user=request.user)
        return queryset

    def get_readonly_fields(self, request, obj=None):
        result = list(super(GoodsModelAdmin, self).get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            result.append('shop')
        return result

    def save_form(self, request, form, change):
        result = super(GoodsModelAdmin, self).save_form(request, form, change)
        if not request.user.is_superuser:
            result.shop = request.user.shop
            result.save()
        return result
