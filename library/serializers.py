from rest_framework import serializers
from .models import Book, Publisher
from django.utils import timezone

from .validators import validate_title_length


# class BookCreateSerializer(serializers.ModelSerializer):
#     discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True, required=False)
#
#     class Meta:
#         model = Book
#         fields = '__all__'

# # Явное определение поля только для чтения
# class BookCreateSerializer(serializers.ModelSerializer):
#     created_at = serializers.DateTimeField(read_only=True)
#     title = serializers.CharField(max_length=100, required=True)
#
#     class Meta:
#         model = Book
#         fields = '__all__'


# Явное определение поля только для чтения. Использование атрибута read_only_fields
class BookCreateSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(required=False)
    title = serializers.CharField(validators=[validate_title_length]) # Пример использования валидатора в сериализаторе
    class Meta:
        model = Book
        fields = ['title', 'author', 'publishing_date', 'price', 'is_bestseller', 'publisher_name']

    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError("Price must be at least 1.")

        return value

    def validate(self, data):
        if data['discounted_price'] and data['discounted_price'] > data['price']:
            raise serializers.ValidationError("Discounted price cannot be higher than the original price.")

        return data

    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()

        publisher_name = validated_data.pop('publisher_name')
        established_date = timezone.now()
        publisher, created = Publisher.objects.get_or_create(name=publisher_name, established_date=established_date)
        book = Book.objects.create(publisher=publisher, **validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Предобработка текстового поля title как заголовок
        if 'title' in validated_data:
            validated_data['title'] = validated_data['title'].strip().title()
        return super().update(instance, validated_data)


# Создание вложенного сериализатора для Publisher
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class BookDetailSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer() # Вложенный сериализатор
    class Meta:
        model = Book
        fields = '__all__'

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']
