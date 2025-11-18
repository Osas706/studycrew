from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# home
def home(request):
  rooms = Room.objects.all()
  context = {'rooms' : rooms}
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
