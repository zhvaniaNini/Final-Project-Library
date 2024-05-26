import random
from django.core.management.base import BaseCommand
from faker import Faker
from datetime import datetime, timedelta
from booklibrary.models import Author, Category, Book

class Command(BaseCommand):
    help = 'Generate random books'

    def handle(self, *args, **kwargs):
        fake = Faker()

        num_authors = 100
        num_books = 1000
        num_categories = 30

        for _ in range(num_authors):
            full_name = fake.name()
            Author.objects.create(full_name=full_name)

        for _ in range(num_categories):
            name = fake.word()
            Category.objects.create(name=name)

        authors = Author.objects.all()
        categories = Category.objects.all()


        for _ in range(num_books):
            author = random.choice(authors)
            category = random.choice(categories)
            title = fake.sentence(nb_words=3)
            publication_date = datetime.now() - timedelta(days=random.randint(1, 365*10)) 
            stock = random.randint(0, 10)

            book = Book.objects.create(
                author=author,
                title=title,
                publication_date=publication_date,
                stock=stock
            )

            book.category.add(category)

            self.stdout.write(self.style.SUCCESS(f'Created book: {title}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated random books.'))