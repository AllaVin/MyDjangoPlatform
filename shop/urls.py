from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.views import CategoryViewSet, SupplierViewSet

# Создаем экземпляр роутера
router = DefaultRouter()

# Регистрируем наш ViewSet.
# 'category' - это префикс URL, по которому будут доступны наши категории.
# CategoryViewSet - представление, которое будет обрабатывать запросы.
router.register('category', CategoryViewSet) # http://127.0.0.1:8000/shop/category/
router.register('supplier', SupplierViewSet) # http://127.0.0.1:8000/shop/supplier/


# Основной список маршрутов нашего приложения.
# Мы просто включаем в него все URL, которые сгенерировал роутер.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
]