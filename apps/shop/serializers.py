from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

from . import models


class LoginSerializer(JSONWebTokenSerializer):

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if not all(credentials.values()):
            raise serializers.ValidationError("用户名和密码是必填字段")

        user = authenticate(**credentials)

        if not user:
            raise serializers.ValidationError("用户名或者密码错误")

        payload = jwt_payload_handler(user)

        return {
            'token': jwt_encode_handler(payload),
            'user': user
        }


class ShopModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = '__all__'

    def create(self, validated_data):
        instance: models.Shop = super(ShopModelSerializer, self).create(validated_data)
        instance.add_location_to_redis()
        return instance


class GoodsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = models.Goods
        exclude = ('update',)
        depth = 1
        extra_kwargs = {
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'shop': {
                'read_only': True
            }
        }

    def get_total_price(self, row):
        return row.price * row.count

    def create(self, validated_data):
        user = validated_data.pop('user')
        shop = user.shop
        validated_data['shop'] = shop
        return super(GoodsSerializer, self).create(validated_data)
