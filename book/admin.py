from django.contrib import admin

from book.models import Book, Comment, Parent

def name(obj):
    return f"{obj.first_name} {obj.last_name}"

class BookAdmin(admin.ModelAdmin):
	list_display = [
		name,
		'slug',
	]




admin.site.register(Book, BookAdmin)
