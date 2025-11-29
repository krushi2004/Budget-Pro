from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Transaction, Category, Profile
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import CustomUserCreationForm

def home(request):
    # Redirect unauthenticated users to login page
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Authenticated users see their dashboard
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(user=request.user)[:5]
    
    # Calculate summary
    income_result = Transaction.objects.filter(
        user=request.user, transaction_type='income'
    ).aggregate(Sum('amount'))
    total_income = income_result['amount__sum'] or 0
    
    expenses_result = Transaction.objects.filter(
        user=request.user, transaction_type='expense'
    ).aggregate(Sum('amount'))
    total_expenses = expenses_result['amount__sum'] or 0
    
    balance = total_income - total_expenses
    
    # Get categories for expenses
    expense_categories = Category.objects.filter(
        transaction__user=request.user,
        transaction__transaction_type='expense'
    ).annotate(total=Sum('transaction__amount')).order_by('-total')
    
    context = {
        'recent_transactions': recent_transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'expense_categories': expense_categories[:5],
    }
    return render(request, 'expenses/home.html', context)

def about(request):
    return render(request, 'expenses/about.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    # Try to get existing profile or create new one
    try:
        profile_obj = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:  # type: ignore
        profile_obj = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Store original email (to prevent changes)
        original_email = request.user.email
        
        # Update user fields (excluding email)
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.username = request.POST.get('username', request.user.username)
        # Email is intentionally not updated for security reasons
        request.user.email = original_email
        
        # Save user object
        try:
            request.user.save()
            messages.success(request, 'Profile information updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile information: {str(e)}')
            return redirect('profile')
        
        # Update profile fields
        profile_obj.phone_number = request.POST.get('phone_number', '')
        profile_obj.occupation = request.POST.get('occupation', '')
        
        if request.POST.get('date_of_birth'):
            try:
                dob_str = request.POST.get('date_of_birth')
                profile_obj.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                messages.warning(request, 'Invalid date format for date of birth.')
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile_obj.profile_picture = request.FILES['profile_picture']
            
        try:
            profile_obj.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
        
        return redirect('profile')
    
    return render(request, 'expenses/profile.html', {'profile': profile_obj})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    
    # Search by title or description
    search_query = request.GET.get('search')
    if search_query:
        transactions = transactions.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Calculate totals
    income_result = transactions.filter(transaction_type='income').aggregate(Sum('amount'))
    total_income = income_result['amount__sum'] or 0
    
    expenses_result = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))
    total_expenses = expenses_result['amount__sum'] or 0
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'search_query': search_query,
    }
    return render(request, 'expenses/transaction_history.html', context)

@login_required
def add_transaction(request):
    # Get all categories initially (for page load)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category_id = request.POST.get('category')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        
        if title and amount and transaction_type and category_id:
            try:
                # Validate that the category matches the transaction type
                category = Category.objects.get(id=category_id, transaction_type=transaction_type)
                transaction = Transaction(
                    user=request.user,
                    title=title,
                    amount=amount,
                    transaction_type=transaction_type,
                    category=category,
                    description=description or ''
                )
                
                # Handle date and time
                if date:
                    # Parse date
                    parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
                    # If time is provided, use it; otherwise use midnight
                    if time:
                        parsed_time = datetime.strptime(time, '%H:%M').time()
                        combined_datetime = datetime.combine(parsed_date, parsed_time)
                    else:
                        combined_datetime = datetime.combine(parsed_date, datetime.min.time())
                    
                    # Make it timezone-aware if USE_TZ is True
                    if timezone.is_naive(combined_datetime):
                        combined_datetime = timezone.make_aware(combined_datetime)
                    transaction.date = combined_datetime  # type: ignore
                transaction.save()
                messages.success(request, 'Transaction added successfully!')
                return redirect('transaction_history')
            except Category.DoesNotExist:  # type: ignore
                messages.error(request, 'Invalid category selected for this transaction type.')
            except ValueError as e:
                messages.error(request, f'Invalid amount or date/time format: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'expenses/add_transaction.html', {'categories': categories})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    # Get all categories initially (for page load)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category_id = request.POST.get('category')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        
        if title and amount and transaction_type and category_id:
            try:
                # Validate that the category matches the transaction type
                category = Category.objects.get(id=category_id, transaction_type=transaction_type)
                transaction.title = title
                transaction.amount = amount
                transaction.transaction_type = transaction_type
                transaction.category = category
                transaction.description = description or ''
                
                # Handle date and time
                if date:
                    # Parse date
                    parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
                    # If time is provided, use it; otherwise use midnight
                    if time:
                        parsed_time = datetime.strptime(time, '%H:%M').time()
                        combined_datetime = datetime.combine(parsed_date, parsed_time)
                    else:
                        combined_datetime = datetime.combine(parsed_date, datetime.min.time())
                    
                    # Make it timezone-aware if USE_TZ is True
                    if timezone.is_naive(combined_datetime):
                        combined_datetime = timezone.make_aware(combined_datetime)
                    transaction.date = combined_datetime  # type: ignore
                transaction.save()
                messages.success(request, 'Transaction updated successfully!')
                return redirect('transaction_history')
            except Category.DoesNotExist:  # type: ignore
                messages.error(request, 'Invalid category selected for this transaction type.')
            except ValueError as e:
                messages.error(request, f'Invalid amount or date/time format: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'expenses/edit_transaction.html', {
        'transaction': transaction,
        'categories': categories
    })

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_history')
    return render(request, 'expenses/delete_transaction.html', {'transaction': transaction})

@login_required
def chart_data(request):
    """API endpoint for chart data"""
    # Income vs Expense data
    income_result = Transaction.objects.filter(
        user=request.user, transaction_type='income'
    ).aggregate(Sum('amount'))
    income = income_result['amount__sum'] or 0
    
    expenses_result = Transaction.objects.filter(
        user=request.user, transaction_type='expense'
    ).aggregate(Sum('amount'))
    expenses = expenses_result['amount__sum'] or 0
    
    # Expense by category
    expense_categories = Category.objects.filter(
        transaction__user=request.user,
        transaction__transaction_type='expense'
    ).annotate(total=Sum('transaction__amount')).order_by('-total')
    
    category_labels = [cat.name for cat in expense_categories]
    category_data = [float(cat.total) for cat in expense_categories]
    
    # Monthly data for last 6 months
    months = []
    monthly_income = []
    monthly_expenses = []
    
    for i in range(5, -1, -1):
        date = timezone.now() - timedelta(days=30*i)
        month_start = date.replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year+1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month+1, day=1) - timedelta(days=1)
            
        months.append(month_start.strftime('%b %Y'))
        
        income_result = Transaction.objects.filter(
            user=request.user,
            transaction_type='income',
            date__gte=month_start,
            date__lte=month_end
        ).aggregate(Sum('amount'))
        income_total = income_result['amount__sum'] or 0
        
        expenses_result = Transaction.objects.filter(
            user=request.user,
            transaction_type='expense',
            date__gte=month_start,
            date__lte=month_end
        ).aggregate(Sum('amount'))
        expense_total = expenses_result['amount__sum'] or 0
        
        monthly_income.append(float(income_total))
        monthly_expenses.append(float(expense_total))
    
    data = {
        'income_expense': {
            'labels': ['Income', 'Expenses'],
            'data': [float(income), float(expenses)]
        },
        'expense_by_category': {
            'labels': category_labels,
            'data': category_data
        },
        'monthly': {
            'labels': months,
            'income': monthly_income,
            'expenses': monthly_expenses
        }
    }
    
    return JsonResponse(data)

def get_categories_by_type(request):
    """AJAX endpoint to get categories by transaction type"""
    transaction_type = request.GET.get('transaction_type')
    if transaction_type:
        categories = Category.objects.filter(transaction_type=transaction_type).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)