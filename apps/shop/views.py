import redis

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_jwt.utils import jwt_response_payload_handler

from . import serializers


class AccountViewSet(GenericViewSet):
    '''登录接口'''

    permission_classes = []

    def get_serializer_class(self):
        return serializers.LoginSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)
        return Response(response_data)


class ShopModelViewSet(ModelViewSet):
    queryset = serializers.models.Shop.objects.all().order_by("-id")

    serializer_class = serializers.ShopModelSerializer

    def filter_queryset(self, queryset):
        '''
        根据地理位置查询附近的店铺, 默认单位为m
        :param queryset:
        :return:
        '''
        queryset = super(ShopModelViewSet, self).filter_queryset(queryset)
        radius = self.request.query_params.get('radius', "0")
        radius = int(radius) if radius.isdigit() else 0

        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        if all([longitude, latitude]):
            try:
                queryset = queryset.model.get_queryset_by_location(queryset, longitude, latitude, radius)
            except redis.exceptions.ResponseError:
                pass
        return queryset


class GoodsModelViewSet(ModelViewSet):
    queryset = serializers.models.Goods.objects.all()
    serializer_class = serializers.GoodsSerializer
    filterset_fields = ('name', 'shop__name', 'is_settle', 'shop__id')

    def get_queryset(self):
        queryset = super(GoodsModelViewSet, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(shop__user=self.request.user)
