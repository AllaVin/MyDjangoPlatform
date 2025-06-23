from django.urls import path
from .views import test

urlpatterns = [
    path('admin', view=test), ## http://127.0.0.1:8000/admin/
    path('library_path', view=test),  # # http://127.0.0.1:8000/library/library_path
]
