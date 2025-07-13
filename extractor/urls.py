from django.urls import path
from .views import extract_email_form_view, dashboard_view, export_contacts_csv

urlpatterns = [
    path('', extract_email_form_view, name='extract_emails'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('export/', export_contacts_csv, name='export_contacts'),
]
