from rest_framework.pagination import CursorPagination

class BookCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-created_at'

