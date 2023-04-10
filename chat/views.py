from django.shortcuts import render, get_object_or_404
from .models import Room


def room(request, pk):
    room: Room = get_object_or_404(Room, pk=pk)
    return render(request, 'chat/room.html', {"room": room, })
