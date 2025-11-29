from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # type: ignore
    name = 'expenses'

    def ready(self):
        try:
            import expenses.signals
        except ImportError:
            pass