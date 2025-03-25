from rest_framework import serializers
from .models import Event, Ticket, UserProfile
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


UserProfile = get_user_model() # Dynamically get custom user when using a custom model

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField() # password won't be exposed and will be write-only

    class Meta:
        model = UserProfile
        fields = '__all__'

    # Describes what will happen when a user registers
    def create(self, validated_data):

        
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            role=validated_data.get('role'),
        )
        
        # Ensure user is saved before creating a token
        user.save()

        # Check if a token already exists for this user
        token, created = Token.objects.get_or_create(user=user)
        
        return user



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