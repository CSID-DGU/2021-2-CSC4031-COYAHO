from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request -> response
def say_hello(request):
    # in real world 
    # 1. pull data from db
    # 2. Transform
    # 3. Send a email
    #return HttpResponse('HELLO WORLD')
    return render(request, 'hello.html', {'name': 'shim'})

