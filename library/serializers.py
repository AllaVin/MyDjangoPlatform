from rest_framework import serializers
from .models import Book, Publisher, Genre
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
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    publisher_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'publishing_date', 'price', 'discounted_price',
                  'is_bestseller', 'genres', 'publisher_name']  # здесь publisher_name допустим

    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError("Price must be at least 1.")
        return value

    def validate(self, data):
        price = data.get('price')
        discounted = data.get('discounted_price')
        if discounted and price and discounted > price:
            raise serializers.ValidationError("Discounted price can't be higher than regular price.")
        return data

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        publisher_name = validated_data.pop('publisher_name')
        publisher, _ = Publisher.objects.get_or_create(name=publisher_name)
        validated_data['publisher'] = publisher
        validated_data['created_at'] = timezone.now()
        book = Book.objects.create(**validated_data)
        book.genres.set(genres)
        return book


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

class BookSerializer(serializers.ModelSerializer):
    # # ______ SlugRelatedField
    # publisher = serializers.SlugRelatedField(slug_field='slug', queryset=Publisher.objects.all())

    # _____ PrimaryKeyRelatedField
    #  publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Book
        fields = '__all__'

    # def validate(self, data):
    #     price = data.get('price')
    #     discounted_price = data.get('discounted_price')
    #
    #     if discounted_price is not None and price is not None:
    #         if discounted_price > price:
    #             raise serializers.ValidationError("Discounted price must be less than or equal to the price.")
    #
    #     return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']