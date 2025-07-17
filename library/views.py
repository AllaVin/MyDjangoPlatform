from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Genre
from .serializers import BookListSerializer, BookDetailSerializer, BookCreateSerializer, GenreSerializer
# from library.models import GENRE_CHOICES
from rest_framework.views import APIView


# Create your views here.
def test(request):
    return HttpResponse("Congrats, you are in Library applications!")

@api_view(['GET', 'POST'])
def book_list_create(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_update_delete(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'},
status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BookDetailSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = BookCreateSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_200_OK)


class GenreChoicesView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def create_genre(request):
    serializer = GenreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,
status=status.HTTP_201_CREATED)
    return Response