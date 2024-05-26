from django.db import models
from Library import settings

# Create your models here.




class Author(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Full Name')

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, verbose_name='Author')
    category = models.ManyToManyField(Category, verbose_name='Category')
    title = models.CharField(max_length=100, verbose_name='Title')
    publication_date = models.DateField(verbose_name='Publication Date')
    stock = models.IntegerField(verbose_name='Stock')
    notify_when_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
      verbose_name = "Book"
      verbose_name_plural = "Books"

    
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book')
    reserved_at = models.DateTimeField(verbose_name='Reserved At')

    def __str__(self):
        return f"{self.user} Reserved {self.book}"
    
    class Meta:
      verbose_name = "Reservation"
      verbose_name_plural = "Reservations"

class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='borrows', on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} Borrowed {self.book}"
    
    class Meta:
      verbose_name = "Borrow"
      verbose_name_plural = "Borrows"


class UserBookNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
    
    class Meta:
      verbose_name = "Book Notification"
      verbose_name_plural = "Book Notifications"
      


