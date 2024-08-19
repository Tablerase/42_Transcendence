from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Game

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = {
        'title': 'Game Test',
        'message': 'Hello, World!',
        'game': Game.objects.all(),
    }
    return HttpResponse(template.render(context, request))