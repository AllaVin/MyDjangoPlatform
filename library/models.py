from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Name")
    last_name = models.CharField(max_length=100, verbose_name="Surname")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    profile = models.URLField(null=True, blank=True, verbose_name="Link to Profile")
    deleted = models.BooleanField(default=False,
                                  verbose_name="If the author is deleted",
                                  help_text="If False - author is active. If True - Author is deleted")
    rating = models.IntegerField(null=True, blank=True, default=1, validators=[MinValueValidator(1), MaxValueValidator(10)],
                                 verbose_name="Rating")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

GENRE_CHOICES = [
    ('db_view_Fiction', 'Fiction'),
    ('db_view_Non-Fiction', 'Non-Fiction'),
    ('db_view_Science Fiction', 'Science Fiction'),
    ('db_view_Fantasy', 'Fantasy'),
    ('db_view_Mystery', 'Mystery'),
    ('db_view_Biography', 'Biography'),
    ('not_set', 'default'),
]

class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Publisher Name")
    established_date = models.DateField(null=True, blank=True, verbose_name="Established Date")

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Book title")
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    publishing_date = models.DateField(verbose_name="Publishing date")
    short_description = models.TextField(null=True, blank=True, verbose_name="Short description")
    genre = models.CharField(choices=GENRE_CHOICES, max_length=50, verbose_name="Genre", default='not_set')
    amount_of_pages = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(10000)],
                                                  verbose_name="Amount of pages", default=50)
    publisher = models.ForeignKey('Member', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Member")
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, verbose_name="Category")
    library = models.ManyToManyField('Library', related_name='books', verbose_name="Library")
    publisher_real = models.ForeignKey('Publisher', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Publisher")
    created_at = models.DateTimeField(null=True, blank=True, verbose_name="Created at")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)

    @property
    def rating(self):
        reviews = self.reviews.all()
        total_reviews = reviews.count()
        if total_reviews == 0:
            return 0
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / total_reviews
        return round(average_rating, 2)


    def __str__(self):
        return f'Book: {self.title} by {self.author}'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category name", unique=True)


    def __str__(self):
        return f'{self.name}'

class Library(models.Model):
    name = models.CharField(max_length=100, verbose_name="Library name")
    location = models.CharField(max_length=100, null=False,blank=False, default="Unknown", verbose_name="Location")
    library_website = models.URLField(null=True, blank=True, verbose_name="Library website")

    def __str__(self):
        return f'Libray: {self.name}'

GENDER_CHOICES = [
    ('Male', 'Male' ),
    ('Female', 'Female' ),
    ('Other', 'Other' ),
]

ROLES_CHOICES = [
    ('Admin', 'Admin' ),
    ('Employee', 'Employee' ),
    ('Reader', 'Reader' ),
]


class Member(models.Model):
    name = models.CharField(max_length=50, verbose_name="Member name")
    surname = models.CharField(max_length=50, blank=True, verbose_name="Member surname")
    email = models.EmailField(null=True, blank=True, verbose_name="Member email", unique=True)
    gender = models.CharField(max_length=50, null=True, blank=True, verbose_name="Gender", choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Age", validators=[MinValueValidator(6), MaxValueValidator(120)],)
    role = models.CharField(max_length=50, null=True, blank=True, verbose_name="Role of member", choices=ROLES_CHOICES)
    is_active = models.BooleanField(default=True, verbose_name="Is active")
    library = models.ManyToManyField('Library', related_name='members', verbose_name="Library used by member")

    def __str__(self):
        return f'{self.name} {self.surname or ""} ({self.role})'


class Posts(models.Model):
    name = models.CharField(max_length=255, verbose_name="Post name", unique=True)
    text = models.TextField(null=True, blank=True, verbose_name="Post text")
    author = models.ForeignKey('Member', null=True, on_delete=models.SET_NULL, verbose_name="Author")
    moderated = models.BooleanField(default=False, verbose_name="Moderated")
    library = models.ForeignKey('Library', null=True, on_delete=models.SET_NULL, related_name='posts', verbose_name="Library")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Created at")
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'Post: {self.name}'


class Borrow(models.Model):
    member = models.ForeignKey('Member', null=True, on_delete=models.SET_NULL, verbose_name="Member", related_name='borrows')
    book = models.ForeignKey('Book', null=True, on_delete=models.SET_NULL, verbose_name="Book")
    library = models.ForeignKey('Library', null=True, on_delete=models.SET_NULL, verbose_name="Library")
    borrow_date = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Borrow date")
    return_date = models.DateField(null=True, blank=True, verbose_name="Return date")
    returned = models.BooleanField(default=False)

    def is_overdue(self):
        if self.returned:
            return False
        return self.return_date < timezone.now().date()


class Review(models.Model):
    book = models.ForeignKey('Book', null=True, on_delete=models.SET_NULL, verbose_name="Book")
    reviewer = models.ForeignKey('Member', null=True, on_delete=models.SET_NULL, verbose_name="Reviewer")
    rating = models.FloatField(null=True, blank=True, verbose_name="Rating")
    feedback = models.TextField(verbose_name="Feedback")

    def __str__(self):
        return f'Review was done for {self.book}'

class AuthorDetail(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='details')
    biography = models.TextField()
    birth_city = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)

    def __str__(self):
        return f'Author info: {self.author}'


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='events')
    books = models.ManyToManyField(Book, related_name='events')

    def __str__(self):
        return f'Event: {self.title}'


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    member = models.ManyToManyField(Member, related_name='event_participations')
    registration_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Participant: {self.event.title}'