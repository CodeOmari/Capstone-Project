from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, AuthViewSet, UpcomingEventViewSet, RegistrationViewSet, OrganizerAttendeesViewSet
from . import views

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'upcoming-events', UpcomingEventViewSet, basename='upcoming-events')
router.register(r'registrations', RegistrationViewSet, basename='registrations')
router.register(r'attendees', OrganizerAttendeesViewSet, basename='attendees')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', views.AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', views.AuthViewSet.as_view({'post': 'login'}), name='login'),
]