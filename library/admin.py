from django.contrib import admin

# Register your models here.
from library.models import Author, Book, Library, Category, Member, Posts, Borrow, Review, AuthorDetail, Event, \
    EventParticipant

admin.site.register(Author)
admin.site.register(Book)
# admin.site.register(Publisher)
# admin.site.register(Library)
admin.site.register(Category)
# admin.site.register(Member) # Здесь закомментировала, така ниже зарегистрировала memer через декаратор
admin.site.register(Posts)
admin.site.register(Borrow)
admin.site.register(Review)
admin.site.register(AuthorDetail)
admin.site.register(Event)
admin.site.register(EventParticipant)

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


