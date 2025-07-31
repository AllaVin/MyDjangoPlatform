Домашнее задание 15  
---
## Замена функций представлений на Generic Views для задач и подзадач

Используя **Generic Views**, замените существующие классы представлений для задач (**Tasks**) и подзадач (**SubTasks**) на соответствующие классы для полного **CRUD** (Create, Read, Update, Delete) функционала. Агрегирующий эндпойнт для статистики задач оставьте как есть. Реализуйте фильтрацию, поиск и сортировку для этих наборов представлений.

---

### Задание 1: Замена представлений для задач (Tasks) на Generic Views

**Шаги для выполнения:**

* **Замените классы представлений для задач на Generic Views:**
    * Используйте `ListCreateAPIView` для создания и получения списка задач.
    * Используйте `RetrieveUpdateDestroyAPIView` для получения, обновления и удаления задач.

* **Реализуйте фильтрацию, поиск и сортировку:**
    * Реализуйте фильтрацию по полям `status` и `deadline`.
    * Реализуйте поиск по полям `title` и `description`.
    * Добавьте сортировку по полю `created_at`.

### Задание 2: Замена представлений для подзадач (SubTasks) на Generic Views

**Шаги для выполнения:**

* **Замените классы представлений для подзадач на Generic Views:**
    * Используйте `ListCreateAPIView` для создания и получения списка подзадач.
    * Используйте `RetrieveUpdateDestroyAPIView` для получения, обновления и удаления подзадач.

* **Реализуйте фильтрацию, поиск и сортировку:**
    * Реализуйте фильтрацию по полям `status` и `deadline`.
    * Реализуйте поиск по полям `title` и `description`.
    * Добавьте сортировку по полю `created_at`.

---

### Оформление ответа

* **Предоставьте решение:** Прикрепите ссылку на гит.
* **Скриншоты тестирования:** Приложите скриншоты из браузера или Postman, подтверждающие успешное создание, обновление, получение и удаление данных через API.


## Задание 1. Ход выполнение: Рефакторинг представлений на Generic Views

---

### Описание задания

Это домашнее задание по рефакторингу проекта на Django Rest Framework.  
Основная цель — заменить стандартные классы представлений для сущностей **Tasks** (Задачи) и **SubTasks** (Подзадачи) на более эффективные и лаконичные **Generic Views**.  
Это позволит обеспечить полный CRUD-функционал (Create, Read, Update, Delete), а также добавить возможности фильтрации, поиска и сортировки.
### 🔧 Шаг 1: Установить (если еще не установлен) и подключить 
`django-filter`

Выполняем команду в терминале:

```bash
  pip install django-filter
```
Открыть файл: 
TaskManager_app/views.py

Найти и удалить (или закомментировать) следующие функции:

- @api_view(['POST']) def new_task(...)  
- @api_view(['GET']) def all_tasks_list(...)  
- @api_view(['GET']) def view_task_by_id(...)

Вставить вместо них вот эти два класса:
```python

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from TaskManager_app.models import Task
from TaskManager_app.serializers import TaskCreateSerializer, TaskByIDSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskByIDSerializer
    lookup_field = 'id'

```
Для тестирования установить Swagger UI

✅ Шаг 1: Установи библиотеку drf-yasg  
Активируй виртуальное окружение и выполни:  
```bash
  pip install drf-yasg
```
✅ Шаг 2: Добавь ``drf_yasg`` в INSTALLED_APPS
В settings.py:
```python 
INSTALLED_APPS = [
    ...
    'drf_yasg',
]
```
Обновить глобальный файл urls (в settings)

```python
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="TaskManager API",
      default_version='v1',
      description="Документация и тестирование API для TaskManager_app",
      contact=openapi.Contact(email="support@example.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    ... # уже имеющиеся пути
    path('admin/', admin.site.urls),
    path('TaskManager_app/', include('TaskManager_app.urls')),

    # Swagger UI:
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc (по желанию):
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```
---
Были заменены классы представлений для задач на Generic Views для следующих операций:
* **CRUD-операции:**
    * **Создание и получение списка задач (`POST` и `GET`):** Используется `ListCreateAPIView`.
    * **Получение, обновление и удаление отдельной задачи (`GET`, `PUT`, `PATCH`, `DELETE`):** Используется `RetrieveUpdateDestroyAPIView`.

* **Расширенный функционал:**
    * **Фильтрация:** Реализована по полям `status` и `deadline`.
    * **Поиск:** Добавлен поиск по полям `title` и `description`.
    * **Сортировка:** Включена сортировка по полю `created_at`.
---


### 2. Замена представлений для подзадач (SubTasks)

Аналогичные изменения были применены к представлениям для подзадач:
Файл ``TaskManager_app/views.py``:
- class SubTaskListCreateView(APIView) и 
- class SubTaskDetailUpdateDeleteView(APIView)  
заменяем на:  
- class SubTaskListCreateView(generics.ListCreateAPIView)
- class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView)

---
### Проверка в Swagger UI

Открываем ссылку `http://127.0.0.1:8000/swagger/``  
Проверим endpoints для запроса **GET /TaskManager_app/subtasks/**  
Добавь параметры в URL:
- /?status=Pending
- /?status=Done&deadline=2025-07-21
- /?ordering=-created_at
- /?search=meeting

📌 Примеры работающих URL:
- Фильтрация по статусу:  
http://127.0.0.1:8000/TaskManager_app/subtasks/?status=Pending  

- Фильтрация по дате дедлайна:  
http://127.0.0.1:8000/TaskManager_app/subtasks/?deadline=2025-07-21  

- Поиск по описанию или названию:  
http://127.0.0.1:8000/TaskManager_app/subtasks/?search=meeting  

- Сортировка по дате создания:  
http://127.0.0.1:8000/TaskManager_app/subtasks/?ordering=-created_at

---

### **Как работает JWT (JSON Web Token)**

```text
[Клиент] --(логин+пароль)--> [Сервер] 
         <-- access + refresh --

[Клиент] --(Bearer access)--> [Сервер] --(проверка токена)--> [Доступ к API]

[Клиент] --(refresh)--> [Сервер] --> [Новый access]

```
---

# Домашнее задание 19.
## Задание 1:  
Извлечение текущего пользователя из запроса
Шаги для выполнения:
- Обновите модели, чтобы включить поле owner.
- Обновите модели Task и SubTask для включения поля owner.
- Измените сериализаторы.
- Измените сериализаторы для моделей Task и SubTask для работы с новым полем.
- Переопределите метод perform_create в представлениях.
- Обновите представления для автоматического добавления владельца объекта.
- Создайте представления для получения задач текущего пользователя.
- Реализуйте представление для получения задач, принадлежащих текущему пользователю.

## Задание 2:  
Реализация пермишенов для API
Шаги для выполнения:
- Создайте пользовательские пермишены.
- Реализуйте пользовательский пермишен для проверки, что пользователь является автором задачи или подзадачи. 
- Примените пермишены к API представлениям. 
- Добавьте пермишены к представлениям для задач и подзадач, чтобы только владельцы могли их изменять или удалять.


## Задание 3:  
Swagger
Шаги для выполнения:
- Установите drf-yasg. 
- Добавьте drf_yasg в settings. 
- Настройте маршруты для Swagger в urls.py. 
- Просмотр документации. 
- Перейдите по URL /swagger/ или /redoc/, чтобы увидеть документацию для вашего API.

---
## Домашнее задание 19. Выполнение  
### TaskManager_app

REST API для управления задачами и подзадачами с JWT-аутентификацией, кастомными пермишенами и автогенерируемой документацией Swagger.

---

### Функционал

- **Задачи и подзадачи** (CRUD)
- **Категории** с мягким удалением и подсчётом количества задач
- **JWT-аутентификация** (SimpleJWT)
- **Кастомные пермишены**: редактировать и удалять задачи может только владелец или администратор
- **Фильтрация, поиск и сортировка**
- **Swagger-документация** (/swagger/)
- **Статистические эндпоинты**:
  - `/task_count/` — общее количество задач
  - `/task_per_status/` — количество задач по статусам
  - `/overdue_tasks_count/` — количество просроченных задач

---

## Установка и запуск

```bash
git clone <repo_url>
cd TaskManager_app
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
## Аутентификация
Получение токена:
> POST /api/token/

```json
{
  "username": "admin",
  "password": "12345"
}
```

Обновление токена:
> POST /api/token/refresh/

Все защищённые эндпоинты требуют заголовка:

> Authorization: Bearer <access_token>  

### Основные эндпоинты
Задачи:
> GET /tasks/ — список всех задач
> 
> GET /tasks/my/ — задачи текущего пользователя
> 
> POST /tasks/ — создать задачу
> 
> GET /tasks/{id}/ — получить задачу PUT /tasks/{id}/ — обновить задачу
> 
> DELETE /tasks/{id}/ — удалить задачу

Подзадачи:
> GET /subtasks/ — список подзадач
> 
> POST /subtasks/ — создать подзадачу
> 
> GET /subtasks/{id}/ — получить подзадачу
> 
> PUT /subtasks/{id}/ — обновить подзадачу
> 
> DELETE /subtasks/{id}/ — удалить подзадачу

Категории:
> GET /categories/
> 
> POST /categories/
> 
> GET /categories/{id}/count_tasks/ — количество задач в категории

Swagger-документация: 
После запуска доступна по адресу: http://127.0.0.1:8000/swagger/  
Примеры тестирования в Postman
- Получить токен → POST /api/token/
- Создать задачу → POST /tasks/ с заголовком Authorization: Bearer <token>
- Получить только свои задачи → GET /tasks/my/
- Удалить чужую задачу → DELETE /tasks/{id}/ (403 если не владелец)
