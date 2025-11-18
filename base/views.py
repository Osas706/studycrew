from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

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
def createroom(request):
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
    
  context = {'form': form}
  return render(request, 'base/room_form.html', context)

# updateroom
def updateroom(request, pk):
  room = Room.objects.get(id=pk)

  form = RoomForm(instance=room)

  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')
    
  context = {'form': form}
  return render(request, 'base/room_form.html', context)

# deleteroom
def deleteroom(request, pk):
  room = Room.objects.get(id=pk)

  if request.method == 'POST':
    room.delete()
    return redirect('home')
    
  return render(request, 'base/delete.html', {'obj': room})
