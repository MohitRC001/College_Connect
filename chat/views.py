from django.shortcuts import render, get_object_or_404
from .models import ChatRoom
from students.models import Student

def chat_room(request, student_id):
    me = request.user.student
    other = get_object_or_404(Student, uid=student_id)

    # Check if room exists
    room = ChatRoom.objects.filter(student1=me, student2=other).first() or ChatRoom.objects.filter(student1=other, student2=me).first()

    if not room:
        room = ChatRoom.objects.create(student1=me, student2=other)

    return render(request, "chat/chat_room.html", {
        "room": room,
        "me": me,
        "other": other,
    })


def chat_home(request):
    return render(request, 'chat/chat_home.html')
