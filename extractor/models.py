from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    email = models.EmailField()
    source = models.CharField(max_length=100)
    contact_type = models.CharField(max_length=20, choices=[
        ('personal', 'Personal'),
        ('business', 'Business'),
        ('spam', 'Spam')
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.contact_type})"