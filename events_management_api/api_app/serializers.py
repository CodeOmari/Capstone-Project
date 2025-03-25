from rest_framework import serializers
from .models import Event, Ticket
from datetime import date



class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'update_at']


    def validate_event_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Event date must be in the future')
        return value






class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id', 'created_at']