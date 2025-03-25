from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('Organizer', 'Organizer'),
        ('Attendee', 'Attendee'),
    ]

    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='Attendee')
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)


    # Add unique related_name attributes to avoid conflicts
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="userprofile_set",  # Custom related_name to avoid clash
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="userprofile_permissions_set",  # Custom related_name to avoid clash
        blank=True
    )


    def __str__(self):
        return f'{self.username} - {self.role}'

    
    class Meta:
        db_table = 'Users'



class Event(models.Model):
    CATEGORY_CHOICES = [
        ('', ''), 
        ('Tech', 'Tech'),
        ('Business', 'Business'),
        ('Social', 'Social'),
        ('Art', 'Art'),
        ('Trade Expos', 'Trade Expos'),
        ('Education', 'Education'),
    ]

    event_title = models.CharField(max_length=100)
    event_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=100)
    virtual_location = models.URLField(blank=True, null=True, default='N/A')
    event_price = models.DecimalField(max_digits=6, decimal_places=2, default='Free')
    event_capacity = models.IntegerField()
    event_organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organizer_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.event_title

    
    class Meta:
        db_table = 'Events'



class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_ticket')
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_attendee')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.attendee.username} - {self.event.event_title}'


    
    class Meta:
        db_table = 'Tickets'