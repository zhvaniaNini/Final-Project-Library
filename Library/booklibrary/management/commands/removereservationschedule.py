from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
import schedule
import time
from booklibrary.models import Reservation


class Command(BaseCommand):
    help = 'Remove Reservation'

    def handle(self, *args, **options):
        
        def remove_reservation():
            threshold_time = datetime.now() - timedelta(minutes=1) 
            expired_reservations = Reservation.objects.filter(reserved_at__lt=threshold_time)

            for reservation in expired_reservations:
                book = reservation.book
                book.stock += 1
                book.save()

            expired_reservations.delete()

            self.stdout.write(self.style.SUCCESS('Deleted expired reservations successfully'))

        schedule.every(1).minutes.do(remove_reservation)

        
        while True:
            schedule.run_pending()
            time.sleep(1)  