from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Tech', 'Tech'),
        ('Business', 'Business'),
        ('Social', 'Social'),
        ('Art', 'Art'),
        ('Trade Expos', 'Trade Expos'),
        ('Education', 'Education'),
    ]

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event_title = models.CharField(max_length=100)
    event_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=100)
    virtual_location = models.URLField(blank=True, null=True, default='N/A')
    event_price = models.DecimalField(max_digits=6, decimal_places=2, default='0.00')
    event_capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.event_title

    
    class Meta:
        db_table = 'Events'



class Registration(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.attendee.username} - {self.event.event_title}'


    
    class Meta:
        db_table = 'Tickets'
        # user can get one ticket for an event
        unique_together = ('event', 'attendee')