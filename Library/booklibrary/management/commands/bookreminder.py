# booklibrary/management/commands/notify_users.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from booklibrary.models import Book, UserBookNotification

class Command(BaseCommand):
    help = 'Sends email notifications to users when books become available.'

    def handle(self, *args, **options):
        available_books = Book.objects.filter(stock__gt=0, notify_when_available=True)
        if not available_books.exists():
            self.stdout.write(self.style.WARNING('No books available for notification.'))
            return
        
        for book in available_books:
            notifications = UserBookNotification.objects.filter(book=book, notified=False)
            if not notifications.exists():
                self.stdout.write(self.style.WARNING(f'No notifications pending for book "{book.title}".'))
                continue
            
            for notification in notifications:
                user = notification.user
                subject = f'Book Available: {book.title}'
                message = f'Dear {user.username},\n\nThe book "{book.title}" by {book.author} is now available. You can borrow it from the library.\n\nThank you,\nThe Library Team'
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email]

                try:
                    send_mail(subject, message, from_email, to_email, fail_silently=False)
                    notification.notified = True
                    notification.save()
                    self.stdout.write(self.style.SUCCESS(f'Notification sent to {user.email} for book "{book.title}"'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to send email to {user.email}: {e}'))
            
            
            book.notify_when_available = False
            book.save()
