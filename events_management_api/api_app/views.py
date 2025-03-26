from django.shortcuts import render
from .serializers import EventSerializer, UserProfileSerializer
from .models import Event
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Token creation handled in the serializer
            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token = user.auth_token.key  # Token directly retrieved
            user_data = UserProfileSerializer(user).data
            return Response({"token": token, "user": user_data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)




class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


    # Ensures only users with Organizer role can create events
    def perform_create(self, serializer):
        if user.request.user.role != 'Organizer':
            raise PermissionDenied("Only Organizers can create events.")
        serializer.save(event_organizer=self.request.user)

    # Ensures Organizers can only update their own events
    def perform_update(self, serializer):
        event = self.get_object()
        if event.event_organizer != self.request.user:
            raise PermissionDenied("You can only update your own events.")
        serializer.save()

    
    def perform_destroy(self, instance):
        if instance.event_organizer != self.request.user:
            raise PermissionDenied("You can only delete your own events")
        instance.delete()


