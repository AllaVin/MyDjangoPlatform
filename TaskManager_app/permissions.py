from rest_framework.permissions import BasePermission

# _____ HW_18. Task 2
# Задание 2: Реализация пермишенов для API
# Шаги для выполнения:
# Продумайте пермишены.
# Продумайте какие пермишены должны быть на представлениях.
# Примените пермишены к API представлениям.
# Добавьте пермишены ко всем представлениям.
# Проверьте что пермишены работают.
# Проверьте что пермишены работают согласно их настройкам.
# Создание кастомного пирмишена. В DRF это делается через написание своего класса через наледование от BasePermission.


class IsAdminOrOwner(BasePermission):
    """
    Доступ разрешён только админу или владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Админ всегда может
        if request.user and (request.user.is_staff or request.user.is_superuser):
            return True
        # Владелец может работать только со своим объектом
        return hasattr(obj, "owner") and obj.owner == request.user
