from django.contrib import admin
from .models import Category, Transaction, Profile

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'transaction_type', 'category', 'user', 'date')
    list_filter = ('transaction_type', 'category', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'occupation', 'date_of_birth', 'created_at')
    search_fields = ('user__username', 'phone_number', 'occupation')
