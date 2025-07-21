from django.shortcuts import render
from rest_framework import viewsets
from shop.models import Category, Supplier
from shop.serializers import CategorySerializer, SupplierSerializer


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




