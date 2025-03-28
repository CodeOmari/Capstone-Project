from .serializers import EventSerializer, UserSerializer
from .models import Event
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
 

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