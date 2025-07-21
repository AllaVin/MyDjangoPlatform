from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.serializers import ProductDetailCreateUpdateSerializer
from shop.views import CategoryViewSet, SupplierViewSet, ProductListCreateView, ProductRetrieveUpdateDestroyView, \
    ProductDetailViewSet, AddressViewSet, CustomerViewSet

# Создаем экземпляр роутера
router = DefaultRouter()

# Регистрируем наш ViewSet.
# 'category' - это префикс URL, по которому будут доступны наши категории.
# CategoryViewSet - представление, которое будет обрабатывать запросы.
router.register('category', CategoryViewSet) # http://127.0.0.1:8000/shop/category/
router.register('supplier', SupplierViewSet) # http://127.0.0.1:8000/shop/supplier/
router.register('product-detail', ProductDetailViewSet) # http://127.0.0.1:8000/shop/product-detail/
router.register('address', AddressViewSet)
router.register('customer', CustomerViewSet)
# Основной список маршрутов нашего приложения.
# Мы просто включаем в него все URL, которые сгенерировал роутер.
urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListCreateView.as_view(), name='product-list-create'), # http://127.0.0.1:8000/shop/products/
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'), # http://127.0.0.1:8000/shop/product-detail/1/
    # Для обновления детальной информации о продукте открыв его с primary key
]