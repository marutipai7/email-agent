from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from extractor.utils import extract_emails, classify_email_type
from .models import Contact
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse


@csrf_exempt
@login_required
def extract_email_form_view(request):
    contacts = []
    if request.method == "POST":
        text = request.POST.get("text", "")
        extracted = extract_emails(text,'form_input')
        for contact in extracted:
            contact_type = classify_email_type(contact.email)
            c = Contact.objects.create(
                email = contact.email,
                source = contact.source,
                contact_type = contact_type,
                user = request.user
            )
            contacts.append(c)
    return render(request, "email_form.html", {"contacts": contacts})


@login_required
def dashboard_view(request):
    contact_list = Contact.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "dashboard.html", {"page_obj": page_obj})

@login_required
def export_contacts_csv(request):
    contacts = Contact.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email', 'Source', 'Contact Type', 'Created At'])
    
    for contact in contacts:
        writer.writerow([contact.email, contact.source, contact.contact_type, contact.created_at])

    return response