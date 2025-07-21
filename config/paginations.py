from rest_framework.pagination import PageNumberPagination, CursorPagination

class BookCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'published_at'