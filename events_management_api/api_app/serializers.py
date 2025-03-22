from rest_framework import serializers
from .models import Event, Ticket

class EventSerializer(serializers.ModelSerializer):
    model = Event
    fields = '__all__'
    read_only_fields = ['id', 'created_at', 'update_at']


class TicketSerializer(serializers.ModelSerializer):
    model = Ticket
    fields = '__all__'
    read_only_fields = ['id', 'created_at']