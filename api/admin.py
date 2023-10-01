from django.contrib import admin
from .models import Book
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "author", "condition", "owner", "status", "created_at", "updated_at", "pickup_location", "previous_owner")