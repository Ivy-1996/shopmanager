from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)

router.register('account', views.AccountViewSet, basename='account')

router.register('shop', views.ShopModelViewSet)

router.register('goods', views.GoodsModelViewSet)

urlpatterns = router.urls
