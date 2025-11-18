from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User

# loginUser
def loginUser(request):
  # redirect user to home page if is_authenticated 
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, 'User does not exist')

    user = authenticate(request, username=username, password=password)

    # if user
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username OR password does not exist')

  context = {}
  return render(request, 'base/auth.html', context)

# logoutUser
def logoutUser(request):
  logout(request)
  return redirect('home')

# home
def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  
  rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) )
  topics = Topic.objects.all()
  room_count = rooms.count()
  context = {
    'rooms' : rooms,
    'topics' : topics,
    'room_count' : room_count,
  }
  return render(request, 'base/home.html', context)

# room
def room(request, pk):
  rooms = Room.objects.get(id=pk)
  context = {'rooms' : rooms}
  return render(request, 'base/room.html', context)

# createroom
@login_required(login_url='login')
def createroom(request):
  form = RoomForm()

  # check if the loggedin user is the same user sending request
  if request.user != room.host:
    return HttpResponse("Your are not allowed here!!!")
  
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
    
  context = {'form': form}
  return render(request, 'base/room_form.html', context)

# updateroom
@login_required(login_url='login')
def updateroom(request, pk):
  room = Room.objects.get(id=pk)

  form = RoomForm(instance=room)
  
  # check if the loggedin user is the same user sending request
  if request.user != room.host:
    return HttpResponse("Your are not allowed here!!!")

  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')
    
  context = {'form': form}
  return render(request, 'base/room_form.html', context)

# deleteroom
@login_required(login_url='login')
def deleteroom(request, pk):
  room = Room.objects.get(id=pk)

  # check if the loggedin user is the same user sending request
  if request.user != room.host:
    return HttpResponse("Your are not allowed here!!!")

  if request.method == 'POST':
    room.delete()
    return redirect('home')
    
  return render(request, 'base/delete.html', {'obj': room})
