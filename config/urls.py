"""
URL configuration for DjangoProject_Library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
# from project.views import test
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token

from config import settings

schema_view = get_schema_view(
   openapi.Info(
      title="TaskManager API",
      default_version='v1',
      description="Документация и тестирование API для TaskManager_app",
      contact=openapi.Contact(email="matyashalla@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls), ## http://127.0.0.1:8000/admin/
    # path("project/", project.urls),
    path('project/', include('project.urls')), ## http://127.0.0.1:8000/admin/project/
    path('library/', include('library.urls')), ## http://127.0.0.1:8000/admin/library/
    path('TaskManager_app/', include('TaskManager_app.urls')), # http://127.0.0.1:8000/admin/TaskManager_app/

    # # _____ HW_15 Task 1. Доюавление путей в рамках выполнения задания
    # Swagger UI:
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), #  Перейти на Swagger UI: http://127.0.0.1:8000/swagger/

    # Redoc (дополнительно):
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # Перейти на Redoc: http://127.0.0.1:8000/redoc/

    # Practicum 8
    # Приложение shop
    path('shop/', include('shop.urls')), # "category": "http://127.0.0.1:8000/shop/category/"
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('TaskManager_app.urls')),  # API эндпоинты
                        # POST /api/token/ — получить токен (нужны username и password).
                        # POST /api/token/refresh/ — обновить токен.

    path('get-token/', obtain_auth_token, name='get_token'), # Маршрут для получения токена
]

