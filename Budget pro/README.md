# Budget Pro - Personal Finance Manager

Budget Pro is a comprehensive web application built with Django that helps users track their income and expenses, manage budgets, and visualize their financial data through interactive charts and reports.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Key Components](#key-components)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Email Configuration](#email-configuration)
- [Customization](#customization)
- [License](#license)

## Features

### Financial Tracking
- Record income and expense transactions
- Categorize transactions for better organization
- Add descriptions and dates to transactions
- View transaction history with filtering and search capabilities

### Dashboard & Analytics
- Real-time balance calculation (Income - Expenses)
- Interactive charts for financial visualization:
  - Income vs Expenses comparison (Pie chart)
  - Expense breakdown by category (Pie chart)
  - Monthly income and expense trends (Bar chart)
- Top expense categories display
- Recent transactions overview

### User Management
- User registration with email verification
- Secure login/logout functionality
- Password reset with OTP verification
- Profile management with personal information
- Profile picture upload capability

### Transaction Management
- Add, edit, and delete transactions
- Filter transactions by type (income/expense) and category
- Search transactions by title or description
- Pagination for large transaction datasets

## Technology Stack

- **Backend**: Django (Python web framework)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Charting**: Chart.js for data visualization
- **Authentication**: Django's built-in authentication system
- **Email**: SMTP for email verification and password reset
- **Styling**: Custom CSS with gradient backgrounds and modern UI components

## Prerequisites

- Python 3.8 or higher
- Django 4.2 or higher
- Pillow library (for image handling)
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd budget-pro
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install django
   pip install Pillow
   ```

## Database Setup

1. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

2. (Optional) Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

3. (Optional) Load default categories:
   ```bash
   python manage.py add_default_categories
   ```

## Running the Application

Start the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to access the application.

## Project Structure

```
budget-pro/
├── budgetpro/              # Main Django project settings
│   ├── settings.py         # Configuration settings
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI deployment configuration
├── expenses/               # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # Application URL routing
│   ├── forms.py            # Form definitions
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JavaScript, images
│   └── management/
│       └── commands/       # Custom management commands
├── media/                  # User uploaded files (profile pictures)
├── db.sqlite3              # SQLite database file
└── manage.py               # Django management script
```

## Key Components

### Models
- **User**: Django's built-in user model for authentication
- **Profile**: Extended user information (phone, date of birth, occupation, profile picture)
- **Category**: Transaction categories with color coding and type (income/expense)
- **Transaction**: Financial records with amount, type, date, and category

### Views
- **Home**: Dashboard with financial summary and charts
- **Profile**: User profile management
- **Transaction History**: List and filter transactions
- **Add/Edit Transaction**: Create and modify transactions
- **Authentication**: Login, signup, and password reset flows

### Templates
- **Base Template**: Common layout with navigation and styling
- **Dashboard**: Financial overview with charts
- **Transaction Management**: Forms and lists for transactions
- **Authentication**: Login, signup, and password reset pages

## API Endpoints

- `GET /api/chart-data/` - Retrieve data for financial charts
- `GET /api/categories-by-type/?transaction_type=<type>` - Get categories filtered by transaction type

## Authentication

Budget Pro implements a complete authentication system:
- User registration with email verification
- Secure login with session management
- Password reset functionality with OTP
- Profile protection (users can only access their own data)

## Email Configuration

For production use, configure the following environment variables:
- `EMAIL_HOST` - SMTP server address
- `EMAIL_PORT` - SMTP server port
- `EMAIL_USE_TLS` - TLS encryption setting
- `EMAIL_HOST_USER` - Email account username
- `EMAIL_HOST_PASSWORD` - Email account password
- `DEFAULT_FROM_EMAIL` - Default sender email address

For Gmail, use an App Password with 2-factor authentication enabled.

## Customization

### Styling
The application uses a custom CSS file (`expenses/static/expenses/css/style.css`) with:
- Modern gradient backgrounds
- Responsive card-based layout
- Interactive hover effects
- Consistent color scheme

### Categories
Default categories can be managed through:
- Django admin interface
- Custom management command (`add_default_categories`)
- Direct database manipulation

## License

This project is proprietary and intended for educational purposes. All rights reserved.