from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader

# Import models
from test.models import Test_User

def test(request):
    users = Test_User.objects.all()
    template = loader.get_template('test.html')
    context = {
        'user': users,
    }
    return HttpResponse(template.render(context, request))