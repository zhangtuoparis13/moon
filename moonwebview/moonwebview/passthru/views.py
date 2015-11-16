from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


#@login_required(login_url='/auth/login/')
@login_required()
def index(request):
    """
    Front interface of the application
    """
    # return render(request, "static/index.html")
    return HttpResponse("MOON")
