from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader

# Import models
from test.models import Test_User

def test(request):
    template = loader.get_template('test.html')

    users = Test_User.objects.all()
    room_name = 'test_room'

    context = {
        'users': users,
        'room_name': room_name,
    }
    return HttpResponse(template.render(context, request))