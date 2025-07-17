from django.contrib import admin
from django.utils import timezone
from library.models import (
    Author, Book, Library, Category, Member, Posts, Borrow,
    Review, AuthorDetail, Event, EventParticipant, Publisher, Genre
)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Posts)
admin.site.register(Borrow)
admin.site.register(Review)
admin.site.register(AuthorDetail)
admin.site.register(Event)
admin.site.register(EventParticipant)

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', "location", "library_website")
    search_fields = ('location',)
    ordering = ('-name',)
    list_per_page = 2

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', "surname", 'email', 'gender', 'date_of_birth', 'age', 'role', 'is_active')
    search_fields = ('surname',)
    ordering = ('name',)
    list_per_page = 2

# Inline книги в админке издателя
class BookInline(admin.TabularInline):
    model = Book
    fk_name = 'publisher'
    extra = 1

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'established_date']
    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'publishing_date', 'is_bestseller')
    list_filter = ('is_bestseller', 'genres')
    search_fields = ('title', 'author__name', 'publisher__name')
    ordering = ('-publishing_date',)
    filter_horizontal = ('genres',)
    actions = ['update_created_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'genre', 'genres', 'short_description')
        }),
        ('Издательство и библиотека', {
            'fields': ('publisher', 'publisher_real', 'category', 'library')
        }),
        ('Даты и статус', {
            'fields': ('publishing_date', 'created_at', 'is_bestseller')
        }),
        ('Цены', {
            'fields': ('price', 'discounted_price')
        }),
    )

    def update_created_at(self, request, queryset):
        queryset.update(created_at=timezone.now())
    update_created_at.short_description = "Update created_at to current time"

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)