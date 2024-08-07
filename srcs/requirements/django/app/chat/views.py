from django.shortcuts import render
from .models import Comment

def home(request):
  context = {
    'comments' : Comment.objects.all()
  }
  return render(request, 'chat/home.html', context)

def about(request):
  return render(request, 'chat/about.html', {'title': "About"})
