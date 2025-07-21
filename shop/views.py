from django.shortcuts import render
from rest_framework import viewsets
from shop.models import Category, Supplier, Product, ProductDetail, Address, Customer, Order
from shop.serializers import CategorySerializer, SupplierSerializer, ProductSerializer, ProductCreateUpdateSerializer, \
    ProductDetailSerializer, ProductDetailCreateUpdateSerializer, AddressSerializer, CustomerSerializer, \
    CustomerCreateUpdateSerializer, OrderSerializer, OrderCreateUpdateSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


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

    def get_serializer_class(self):
        # Для чтения данных
        if self.request.method == 'GET':
            return ProductSerializer
        # Для изменения или удаления (PUT, PATCH, DELETE)
        return ProductCreateUpdateSerializer

class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()

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

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerSerializer
        return CustomerCreateUpdateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        return OrderCreateUpdateSerializer