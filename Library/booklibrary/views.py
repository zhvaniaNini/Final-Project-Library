from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from booklibrary.models import Book, Borrow, Reservation, UserBookNotification
from django.core.paginator import Paginator
from booklibrary.serializers import CreateBookSerializer, UpdateBookSerializer, DeleteBookSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Count
from django.db.models import F, Sum,ExpressionWrapper, DurationField, IntegerField

# Create your views here.
def home(request):
    return render(request, 'home.html')

def book_list(request):
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 50)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    return render(request, 'book_list.html', {'books': books})

def in_demand(request):
    books_list = Book.objects.annotate(num_borrows=Count('borrows')).order_by('-num_borrows')
    paginator = Paginator(books_list, 50)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    borrows = Borrow.objects.filter(book=book)
    borrow_count = borrows.count()

    one_year_ago = datetime.now() - timedelta(days=365)
    borrows_last_year = borrows.filter(borrowed_at__gte=one_year_ago)
    
    borrow_stats = borrows_last_year.count()
    return render(request, 'book_detail.html', {'book': book, 'borrow_count': borrow_count, 'borrow_stats':borrow_stats})


def search_books(request):
    query = request.GET.get('q')
    if query:
        books_list = Book.objects.filter(title__icontains=query)
    else:
        books_list = Book.objects.none() 

    if books_list.exists() and books_list.count() > 50:
        paginator = Paginator(books_list, 50)
        page = request.GET.get('page')
        books = paginator.get_page(page)
    else:
        books = books_list
    return render(request, 'search_books.html', {'books': books, 'query': query})


def most_popular_books(request):
    books = Book.objects.annotate(num_borrows=Count('borrows')).order_by('-num_borrows')[:10]
    return render(request, 'book_list.html', {'books': books})


def most_late_books(request):
    late = timedelta(days=10)

    late_borrows = Borrow.objects.annotate(
        days_late=ExpressionWrapper(
            F('returned_at') - F('borrowed_at') - late,
            output_field=DurationField()
        )
    ).filter(
        returned_at__isnull=False,
        days_late__gt=timedelta(days=0) 
    )

    top_books = late_borrows.values('book__id', 'book__title', 'book__author__full_name').annotate(
        late_count=Count('id'),
        total_days_late=Sum('days_late')
    ).order_by('-total_days_late')[:100]

    books = [
        {
            'id': entry['book__id'],
            'title': entry['book__title'],
            'author': entry['book__author__full_name'],
            'late_count': entry['late_count'],
            'total_days_late': entry['total_days_late'].days  
        }
        for entry in top_books
    ]
    return render(request, 'book_list.html', {'books': books})


@login_required
def notify(request, book_id):
    book = Book.objects.get(pk=book_id)
    notification_exists = UserBookNotification.objects.filter(book=book, user=request.user, notified=False).exists()

    if not notification_exists:
        UserBookNotification.objects.create(book=book, user=request.user)
        book.notify_when_available = True
        book.save()

        messages.success(request, 'You will be notified when the book becomes available.')
    else:
        messages.info(request, 'You have already opted in to be notified for this book.')

    return render(request, 'home.html')
    

@staff_member_required
def late_user(request):
    late = timedelta(days=10)

    late_borrows = Borrow.objects.annotate(
        days_late=ExpressionWrapper(
            F('returned_at') - F('borrowed_at') - late,
            output_field=DurationField()
        )
    ).filter(
        returned_at__isnull=False,
        days_late__gt=timedelta(days=0) 
    )
    users = late_borrows.values('user__username').annotate(
        late_count=Count('id'),
        total_days_late=Sum('days_late')
    ).order_by('-total_days_late')[:100]

    return render(request, 'top_late_users.html', {'users': users})


@login_required
def profile(request):
    profile = request.user.profile
    reservations = Reservation.objects.filter(user=request.user)
    borrowed = Borrow.objects.filter(user=request.user, returned_at__isnull=True)
    books = Book.objects.filter(notify_when_available=True)
    return render(request, 'profile.html', {'profile':profile, 'reservations':reservations, 'borrowed':borrowed, 'books':books})


@login_required
def reservation(request, book_id):
    book = Book.objects.get(pk=book_id)
    existing_reservation = Reservation.objects.filter(user=request.user, book=book).exists()
    existing_borrow = Borrow.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists()
    if existing_reservation or existing_borrow:
        messages.error(request, "You have already reserved or borrowed this book")
        return redirect('book_detail', book_id=book_id)
    if book.stock > 0:
        reserve_date = datetime.now()
        reservation = Reservation.objects.create(user=request.user, book=book, reserved_at=reserve_date)
        book.stock -= 1
        book.save()
    else:
        message = "No stock available for reservation."
    return render(request, 'reservation.html', {'book': book})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    reservation = Reservation.objects.filter(book=book, user=request.user).first()
    if reservation:
        reservation.delete()
    existing_reservation = Reservation.objects.filter(user=request.user, book=book).exists()
    existing_borrow = Borrow.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists()
    if existing_reservation or existing_borrow:
        messages.error(request, "You have already reserved or borrowed this book")
        return redirect('book_detail', book_id=book_id)
    if book.stock > 0:
        borrow_date = datetime.now()
        borrow = Borrow.objects.create(user=request.user, book=book, borrowed_at=borrow_date)
        book.stock -= 1
        book.save()
    return render(request, 'borrow.html', {'book': book, 'borrow_date':borrow_date})

@staff_member_required
def return_book(request, borrow_id):
    borrow = Borrow.objects.get(pk=borrow_id)
    book = borrow.book
    if not borrow.returned_at:
        borrow.returned_at = datetime.now()
        borrow.save()
        book.stock += 1
        book.save()
        messages.success(request, ("Successfully Registered Return!"))
        return redirect('borrows')
    else:
        messages.error(request, "Invalid Return Request!")

    return render(request, 'borrows.html', {'book': book})

@staff_member_required
def borrows(request):
    borrows = Borrow.objects.all()
    return render(request, 'borrows.html', {'borrows':borrows})


@staff_member_required
def borrow_history(request, book_id):
    book = Book.objects.get(pk=book_id)
    borrows = Borrow.objects.filter(book=book)
    borrow_count = borrows.count()
    count = 0
    for borrow in borrows:
        if borrow.returned_at is None:
            count +=1
    return render(request, 'borrowhistory.html', {'book':book, 'borrows':borrows, 'borrow_count':borrow_count, 'not_returned_count':count})


@method_decorator(staff_member_required, name='dispatch')    
class CreateBook(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = CreateBookSerializer

@method_decorator(staff_member_required, name='dispatch')
class UpdateBook(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = UpdateBookSerializer
    lookup_url_kwarg = 'book_id'

@method_decorator(staff_member_required, name='dispatch')
class DeleteBook(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = DeleteBookSerializer
    lookup_url_kwarg = 'book_id'

