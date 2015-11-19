from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from moonwebview.server import settings


#@login_required(login_url='/auth/login/')
@login_required()
def index(request):
    """
    Front interface of the application
    """
    # return render(request, "static/index.html")
    from django.contrib.auth import get_user_model
    from django.contrib.auth import get_user
    print(get_user_model())
    print(get_user(request))
    print(request)
    return HttpResponse("MOON -{}-".format(get_user(request)))


@login_required()
def passthru(request, url=None):
    """
    Front interface of the application
    """
    # TODO: set an applicative FW to limit the use of the API
    # return render(request, "static/index.html")
    from django.contrib.auth import get_user_model
    from django.contrib.auth import get_user
    print(get_user_model())
    print(get_user(request))
    print(request)
    return HttpResponse("MOON -user={}- Will send a request to {}/{}".format(
        get_user(request), settings.OPENSTACK_KEYSTONE_URL, url))
