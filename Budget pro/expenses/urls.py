from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import email_views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', email_views.signup_with_email_verification, name='signup'),
    path('verify-email/', email_views.verify_email, name='verify_email'),
    path('resend-verification/', email_views.resend_verification, name='resend_verification'),
    path('password-reset/', email_views.password_reset_request, name='password_reset'),
    path('password-reset/verify/', email_views.password_reset_verify, name='password_reset_verify'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Transactions
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('transactions/delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    
    # API endpoints
    path('api/chart-data/', views.chart_data, name='chart_data'),
    path('api/categories-by-type/', views.get_categories_by_type, name='categories_by_type'),
]