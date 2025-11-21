from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.loginUser, name='login'),
  path('register/', views.registerUser, name='register'),
  path('logout/', views.logoutUser, name='logout'),

  path('', views.home, name='home'),
  path('room/<str:pk>/', views.room, name='room'),
  path('profile/<str:pk>/', views.userprofile, name='user-profile'),

  path('create-room/', views.createroom, name='create-room'),
  path('update-room/<str:pk>/', views.updateroom, name='update-room'),
  path('delete-room/<str:pk>/', views.deleteroom, name='delete-room'),

  path('delete-message/<str:pk>/', views.deletemessage, name='delete-message'),
]