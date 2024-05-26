from django.contrib import admin
from booklibrary.models import Author, Category, Book, Borrow, Reservation, UserBookNotification

# Register your models here.
@admin.register(Author)
class BookAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    search_fields = ['full_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(Borrow)   
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned_at')
    fields = ('user', 'book', 'borrowed_at', 'returned_at')
    list_filter = ('returned_at',)
    search_fields = ('user__username', 'book__title')


admin.site.register(Category)
admin.site.register(Reservation)
admin.site.register(UserBookNotification)
