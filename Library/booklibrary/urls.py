from django.urls import path
from booklibrary.views import CreateBook, UpdateBook, DeleteBook
from booklibrary import views

urlpatterns = [
    path('home/', views.home, name='home_page'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.search_books, name='search_books'),
    path('reserve/<int:book_id>/', views.reservation, name='reservation'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('create/', CreateBook.as_view(), name='create'),
    path('update/<int:book_id>/', UpdateBook.as_view(), name='update'),
    path('delete/<int:book_id>/', DeleteBook.as_view(), name='delete'),
    path('profile/', views.profile, name='user_profile'),
    path('borrowhistory/<int:book_id>/', views.borrow_history, name='borrow_history'),
    path('borrows/', views.borrows, name='borrows'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('popularbooks/', views.most_popular_books, name='most_popular_books'),
    path('latebooks/', views.most_late_books, name='most_late_books'),
    path('lateusers/', views.late_user, name='most_late_users'),
    path('notify/<int:book_id>/', views.notify, name='notify'),
    path('sort/', views.in_demand, name='in_demand')
]