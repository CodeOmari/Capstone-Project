from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Registration
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    # ensures password is not exposed in API responses and is strong
    password = serializers.CharField(write_only=True, validators=[validate_password])
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Hash passwords before saving the user
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
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
    event_title = serializers.CharField(source='event.event_title', read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'attendee', 'event', 'event_title', 'phone_number', 'registered_at']
        read_only_fields = ['id', 'registered_at']

    def validate(self, data):
        user = self.context['request'].user
        event = data.get('event')

        if Registration.objects.filter(attendee=user, event=event).exists():
            raise serializers.ValidationError("You are already registered for this event.")

        if event.organizer == user:
            raise serializers.ValidationError("You cannot register for your own event.")

        return data