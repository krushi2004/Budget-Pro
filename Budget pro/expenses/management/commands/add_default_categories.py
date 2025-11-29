from django.core.management.base import BaseCommand
from expenses.models import Category


class Command(BaseCommand):
    help = 'Add default categories to the database'

    def handle(self, *args, **kwargs):
        # Expense categories
        expense_categories = [
            {'name': 'Food & Dining', 'color': '#FF6384', 'transaction_type': 'expense'},
            {'name': 'Transportation', 'color': '#36A2EB', 'transaction_type': 'expense'},
            {'name': 'Entertainment', 'color': '#FFCE56', 'transaction_type': 'expense'},
            {'name': 'Rent & Housing', 'color': '#4BC0C0', 'transaction_type': 'expense'},
            {'name': 'Utilities', 'color': '#9966FF', 'transaction_type': 'expense'},
            {'name': 'Shopping', 'color': '#FF9F40', 'transaction_type': 'expense'},
            {'name': 'Healthcare', 'color': '#FF6384', 'transaction_type': 'expense'},
            {'name': 'Education', 'color': '#4BC0C0', 'transaction_type': 'expense'},
            {'name': 'Other', 'color': '#6C757D', 'transaction_type': 'expense'},
        ]

        # Income categories
        income_categories = [
            {'name': 'Salary', 'color': '#28A745', 'transaction_type': 'income'},
            {'name': 'Freelance', 'color': '#17A2B8', 'transaction_type': 'income'},
            {'name': 'Investment', 'color': '#6F42C1', 'transaction_type': 'income'},
            {'name': 'Gift', 'color': '#E83E8C', 'transaction_type': 'income'},
            {'name': 'Other Income', 'color': '#6C757D', 'transaction_type': 'income'},
        ]

        all_categories = expense_categories + income_categories
        created_count = 0
        
        for cat_data in all_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                transaction_type=cat_data['transaction_type'],
                defaults={'color': cat_data['color']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name} ({category.transaction_type})')  # type: ignore
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name} ({category.transaction_type})')  # type: ignore
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal categories created: {created_count}')  # type: ignore
        )