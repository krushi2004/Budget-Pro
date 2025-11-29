from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from typing import Any


class Profile(models.Model):
    # Add type hint for the objects manager to satisfy static type checkers
    objects: models.Manager
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        # Using getattr to avoid linter warnings
        username = getattr(self.user, 'username', 'Unknown')
        return f"{username}'s Profile"

class Category(models.Model):
    # Add type hint for the objects manager to satisfy static type checkers
    objects: models.Manager
    
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#007bff')  # For UI visualization
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='expense')
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self) -> str:
        return f"{self.name} ({self.transaction_type})" if self.name else "Unnamed Category"

class Transaction(models.Model):
    # Add type hint for the objects manager to satisfy static type checkers
    objects: models.Manager
    
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self) -> str:
        return f"{self.title} - {self.amount}" if self.title and self.amount else "Unnamed Transaction"