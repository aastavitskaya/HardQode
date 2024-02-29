from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from courses.views import ProductViewSet, LessonViewSet, ProductStatsViewSet, GroupMembershipViewSet

router = routers.DefaultRouter()
router.register('products-stat', ProductStatsViewSet, basename='product-stats')
router.register('products', ProductViewSet, basename='products')
products_router = NestedSimpleRouter(router, 'products', lookup='product')
products_router.register('subscribe', GroupMembershipViewSet, basename='subscribe')
products_router.register('lessons', LessonViewSet, basename='product-lessons')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(products_router.urls)),
    path('admin/', admin.site.urls),
]
