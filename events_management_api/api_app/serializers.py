from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Registration
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password1']
        )
        return user



class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.CharField(source='organizer.username', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'update_at', 'organizer']


    def validate_event_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Event date must be in the future')
        return value




class RegistrationSerializer(serializers.ModelSerializer):
    attendee = serializers.HiddenField(default=serializers.CurrentUserDefault())
    attendee_name = serializers.SerializerMethodField()
    event_title = serializers.CharField(source='event.event_title', read_only=True)


    class Meta:
        model = Registration
        fields = ['id', 'attendee', 'attendee_name', 'event', 'event_title', 'phone_number', 'registered_at']
        read_only_fields = ['id', 'registered_at']

    def get_attendee_name(self, obj):
        return obj.attendee.username if obj.attendee else None

    def validate(self, data):
        user = self.context['request'].user
        event = data.get('event')

        if Registration.objects.filter(attendee=user, event=event).exists():
            raise serializers.ValidationError("You are already registered for this event.")

        if event.organizer == user:
            raise serializers.ValidationError("You cannot register for your own event.")

        return data



