from .serializers import EventSerializer, UserSerializer, RegistrationSerializer
from .models import Event, Registration
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import date, timedelta
from django.db.models import F


 

# Create your views here.
class AuthViewSet(viewsets.ViewSet):

    # allow anyone to register or login
    permission_classes = [AllowAny]
    
    def register(self, request):
        serializer = UserSerializer(data=request.data)
     
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
    def login(self, request):
        username= request.data.get('username')
        password= request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message":"login successful", 'token':token.key}, status=status.HTTP_200_OK)
        return Response({"error":"incorrect username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
class IsEventOrganizerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the event organizer
        return obj.organizer == request.user


class EventViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, IsEventOrganizerOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
   
    # organizers only see the events they own
    # Other users can see all events
    def get_queryset(self):
        user = self.request.user
        if Event.objects.filter(organizer=user).exists():
            return Event.objects.filter(organizer=user)
        return Event.objects.all()






class UpcomingEventViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_queryset(self):
        today = date.today()
        five_days_later = today + timedelta(days=5)

        queryset = Event.objects.filter(event_date__range=(today, five_days_later))

        title = self.request.query_params.get('title')
        location = self.request.query_params.get('location')
        category = self.request.query_params.get('category')

        if title:
            queryset = queryset.filter(event_title__icontains=title)
        if location:
            queryset = queryset.filter(Q(event_location__icontains=location) | Q(virtual_location__icontains=location))
        if category:
            queryset = queryset.filter(event_category__iexact=category)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # If user is an organizer, show only their events
        user = request.user
        user_events = queryset.filter(organizer=user)

        if user_events.exists():
            serializer = self.get_serializer(user_events, many=True)
            return Response(serializer.data)

        if not queryset.exists():
            return Response({"message": "No upcoming events within the next 5 days."}, status=200)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




# Only ticket owners to update or delete their tickets
class IsTicketOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.attendee == request.user


class RegistrationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsTicketOwner]
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return Registration.objects.filter(attendee=self.request.user)

    def perform_create(self, serializer):
        serializer.save(attendee=self.request.user)


# To show list of attendees for an event
class OrganizerAttendeesViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        return Registration.objects.filter(event__organizer=user)