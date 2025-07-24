from django.shortcuts import render
from rest_framework import viewsets
from shop.models import Category, Supplier, Product, ProductDetail, Address, Customer, Order, OrderItem
from shop.serializers import CategorySerializer, SupplierSerializer, ProductSerializer, ProductCreateUpdateSerializer, \
    ProductDetailSerializer, ProductDetailCreateUpdateSerializer, AddressSerializer, CustomerSerializer, \
    CustomerCreateUpdateSerializer, OrderSerializer, OrderCreateUpdateSerializer, OrderItemSerializer, \
    OrderItemCreateUpdateSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Это представление предоставляет полный набор действий (CRUD) для модели Category.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



class SupplierViewSet(viewsets.ModelViewSet):
    """
    Это представление предоставляет полный набор действий (CRUD) для модели Supplier.
    """
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


class ProductListCreateView(ListCreateAPIView):
    """
    Представление для получения списка продуктов и создания нового продукта.
    """
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'price'] # Пример ссылки с фильтрацией по категории http://127.0.0.1:8000/shop/product/?category=1

    # Явно указываем классы аутентификации для этого представления.
    # Это переопределит глобальные настройки, если они есть.
    # authentication_classes = [BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    # Явно указываем классы разрешений для этого представления.
    # Пользователь должен быть аутентифицирован для доступа.
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Этот метод позволяет нам динамически выбирать сериалайзер
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких как GET
        if self.request.method == 'GET':
            return ProductSerializer
        # Для остальных методов (POST)
        return ProductCreateUpdateSerializer

class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления одного продукта.
    """
    queryset = Product.objects.all()

    # Явно указываем классы разрешений для этого представления.
    # Пользователь должен быть аутентифицирован для доступа.
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        # Для чтения данных
        if self.request.method == 'GET':
            return ProductSerializer
        # Для изменения или удаления (PUT, PATCH, DELETE)
        return ProductCreateUpdateSerializer

class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()

    # Явно указываем классы разрешений для этого представления.
    # Пользователь должен быть аутентифицирован для доступа.
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Этот метод позволяет нам динамически выбирать сериалайзер
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких, как GET
        if self.request.method == 'GET':
            return ProductDetailSerializer
        # Для остальных методов
        return ProductDetailCreateUpdateSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    # Явно указываем классы разрешений для этого представления.
    # Пользователь должен быть аутентифицирован для доступа.
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']

    # Явно указываем классы разрешений для этого представления.
    # Пользователь должен быть аутентифицирован для доступа.
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerSerializer
        return CustomerCreateUpdateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    # Явно указываем классы разрешений для этого представления.
    # Пользователь должен быть аутентифицирован для доступа.
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        return OrderCreateUpdateSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()

    # Явно указываем классы разрешений для этого представления.
    # Пользователь должен быть аутентифицирован для доступа.
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderItemSerializer
        return OrderItemCreateUpdateSerializer