from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'age', 'course', 'created_at']
    list_filter = ['course', 'age', 'created_at']
    search_fields = ['name', 'email', 'course']
    readonly_fields = ['created_at', 'updated_at']