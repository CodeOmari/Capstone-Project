from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, AuthViewSet
from . import views

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('register/', views.AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', views.AuthViewSet.as_view({'post': 'login'}), name='login'),
]