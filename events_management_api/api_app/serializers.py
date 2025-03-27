from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Ticket
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
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