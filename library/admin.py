# Register your models here.
from library.models import Author, Book, Library, Category, Member, Posts, Borrow, Review, AuthorDetail, Event, \
    EventParticipant, Publisher
from django.contrib import admin

admin.site.register(Author)
# admin.site.register(Book) # Здесь закомментировала, така ниже зарегистрировала memer через декаратор
# admin.site.register(Publisher) # Здесь закомментировала, така ниже зарегистрировала memer через декаратор
# admin.site.register(Library) # Здесь закомментировала, така ниже зарегистрировала memer через декаратор
admin.site.register(Category)
# admin.site.register(Member) # Здесь закомментировала, така ниже зарегистрировала memer через декаратор
admin.site.register(Posts)
admin.site.register(Borrow)
admin.site.register(Review)
admin.site.register(AuthorDetail)
admin.site.register(Event)
admin.site.register(EventParticipant)

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title',
#                     'author',
#                     'publisher_real',)
#     ordering = ('-title',)
#     list_per_page = 10
#
#
# @admin.register(Publisher)
# class PublisherAdmin(admin.ModelAdmin):
#     list_display = ('name',
#                     'established_date',)
#     ordering = ('-name',)
#     list_per_page = 10


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',
                    "location",
                    "library_website")
    search_fields = ('location',)
    ordering = ('-name',)
    list_per_page = 2


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name',
                    "surname",
                    'email',
                    'gender',
                    'date_of_birth',
                    'age',
                    'role',
                    'is_active',)
    search_fields = ('surname',)
    ordering = ('name',)
    list_per_page = 2


## _____ Настройка инлайн-форм с использованием TabularInline
## Закомментируем Book и Publisher выше

# from django.contrib import admin
# from .models import Book, Publisher

# class BookInline(admin.TabularInline): ## Book - встраивается в отображение Publisher
#     model = Book
#     extra = 1
# class PublisherAdmin(admin.ModelAdmin): ## Открыв Publisher, у нас будет возможность редактировать его книги
#     inlines = [BookInline]
#
# admin.site.register(Publisher, PublisherAdmin)
# admin.site.register(Book)


# _____ Настройка инлайн-форм с использованием StackedInline
# Закомментируем Book и Publisher с использованием TabularInline выше

class BookInline(admin.StackedInline):
    model = Book
    extra = 1

class PublisherAdmin(admin.ModelAdmin):
    inlines = [BookInline] ## В Publisher встреивается Books. Открываешь Publisher -> можешь редактировать Books

admin.site.register(Publisher, PublisherAdmin)
# admin.site.register(Book)


# ## _____ Обновления поля created_at у выбранных книг на текущее время.
from django.utils import timezone  # NEW IMPORT

class BookAdmin(admin.ModelAdmin):
    def update_created_at(self, request, queryset):
        queryset.update(created_at=timezone.now())
    update_created_at.short_description = "Update created_at to current time"
    # other fields ...
    actions = [update_created_at]  # NEW FIELD

## Зарегистрируем правильно BookAdmin через @admin.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def update_created_at(self, request, queryset):
        queryset.update(created_at=timezone.now())
    update_created_at.short_description = "Update created_at to current time"
    actions = [update_created_at]
