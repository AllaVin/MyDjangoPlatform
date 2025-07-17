from django.urls import path
from .views import test, book_list_create, book_detail_update_delete, create_genre
from .views import GenreChoicesView

urlpatterns = [
    path('admin', view=test), ## http://127.0.0.1:8000/admin/
    path('library_path', view=test),  # # http://127.0.0.1:8000/library/library_path
    path('books/', book_list_create, name='book-list-create'), # Для получения всех книг и создания новой книги - http://127.0.0.1:8000/library/books/
    path('books/<int:pk>/', book_detail_update_delete, name='book-detail-update-delete'), # Для операций с одной книгой
    # path('genres/', GenreChoicesView.as_view(), name='genre-choices'), # http://127.0.0.1:8000/library/genres/

    path('genres/', create_genre, name='create-genre'), # Маршрут для создания жанров
]
