from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader

# Import models
from test.models import Test_User

def index(request):
    return HttpResponse("Hello, world. You're at the test index.")

def test(request, room_name):
    template = loader.get_template('test.html')

    users = Test_User.objects.all()

    context = {
        'users': users,
        'room_name': room_name,
    }
    return HttpResponse(template.render(context, request))