from django.shortcuts import render
from .serializers import EventSerializer
from .models import Event
from rest_framework import viewsets

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer