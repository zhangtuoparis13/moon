from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings as dsettings

from django.http import HttpResponse
from openstack_auth.utils import get_keystone_client
from moon import settings
from openstack_auth.backend import KeystoneBackend
from keystoneclient.v3 import client


def get_keystone_client(request):
    c = client.Client(
        token=request.user.token.id,
        endpoint=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
        original_ip=request.environ.get('REMOTE_ADDR', ''),
        insecure=True,
        cacert=None,
        auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
        debug=settings.DEBUG
    )
    return c

@login_required(login_url='/auth/login/')
def index(request):
    """
    Front interface of the application
    """
    return render(request, "moon/base_site.html")

@login_required(login_url='/auth/login/')
def users(request):
    """
    Users interface
    Render all (or some) users retrieve from OpenStack Keystone server
    """

    c = get_keystone_client(request)
    # print(c.roles.list())
    all_users = c.users.list()
    return render(request, "moon/users.html", {"users": all_users})

@login_required(login_url='/auth/login/')
def projects(request):
    """
    Users interface
    Render all (or some) users retrieve from OpenStack Keystone server
    """

    c = get_keystone_client(request)
    # print(c.projects.list())
    all_users = c.projects.list()
    return render(request, "moon/projects.html", {"projects": all_users})

@login_required(login_url='/auth/login/')
def roles(request):
    """
    Users interface
    Render all (or some) users retrieve from OpenStack Keystone server
    """

    c = get_keystone_client(request)
    # print(c.roles.list())
    all_users = c.roles.list()
    return render(request, "moon/roles.html", {"roles": all_users})
