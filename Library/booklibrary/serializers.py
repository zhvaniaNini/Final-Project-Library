from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from booklibrary.models import Book


class CreateBookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

class UpdateBookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = ['stock']

class DeleteBookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


