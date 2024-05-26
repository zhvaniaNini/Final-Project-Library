from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from booklibrary.models import Borrow
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends email reminders for late book returns'

    def handle(self, *args, **options):
    
        ten_days_ago = timezone.now() - timedelta(days=10)

        
        late_borrows = Borrow.objects.filter(returned_at__isnull=True, borrowed_at__lte=ten_days_ago)

        for late_borrow in late_borrows:
            
            if late_borrow.borrowed_at:
                
                days_late = (timezone.now() - late_borrow.borrowed_at).days

                subject = 'Reminder: Late Book Return'
                message = f'Dear {late_borrow.user.username},\n\nYou have borrowed the book "{late_borrow.book.title}" and it is now overdue by {days_late} days. Please return it to the library as soon as possible.\n\nThank you,\nThe Library Team'
                from_email = settings.EMAIL_HOST_USER  
                to_email = [late_borrow.user.email]

                
                try:
                    send_mail(subject, message, from_email, to_email, fail_silently=False)
                    self.stdout.write(self.style.SUCCESS(f'Email reminder sent successfully to {late_borrow.user.email}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to send email reminder to {late_borrow.user.email}: {e}'))
            else:
                self.stdout.write(self.style.ERROR(f'Skipping late borrow with ID {late_borrow.id}: borrowed_at is None'))

        self.stdout.write(self.style.SUCCESS('Email reminders processed successfully'))
