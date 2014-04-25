from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#from openstack_auth.utils import get_keystone_client
from gi import settings
from keystoneclient.v3 import client
from keystoneclient.v3.users import User

from core.pap.core import PAP

import logging

logger = logging.getLogger("moon.django")


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

from django import forms


class UserAddForm(forms.Form):
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    domain = forms.CharField(max_length=100, initial="Default")
    project = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=100, required=False)
    description = forms.CharField(max_length=100, required=False)
    enable = forms.BooleanField(initial=True)

@login_required(login_url='/auth/login/')
def user(request, id=None):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    pap = PAP(kclient=get_keystone_client(request))
    user = pap.get_user(uuid=id)
    return render(request, "moon/users.html", {"user": user})


@login_required(login_url='/auth/login/')
def users(request):
    """
    Users interface
    Render all (or some) users retrieve from OpenStack Keystone server
    """
    pap = PAP(kclient=get_keystone_client(request))
    form = UserAddForm()
    result = None
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            domain = form.cleaned_data['domain']
            project = form.cleaned_data['project']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            enable = form.cleaned_data['enable']
            if password1 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            result = pap.users.create(
                name=username,
                password=password1,
                domain=domain,
                project=project,
                email=email,
                description=description,
                enabled=enable
            )
            if type(result) is User:
                result = "User Created"
        else:
            raise forms.ValidationError("Form is not complete.")
    all_users = sorted(pap.users.list(), key=lambda _user: _user.name)
    return render(request, "moon/users.html", {"users": all_users, "form": form, "result": result})

@login_required(login_url='/auth/login/')
def projects(request):
    """
    Users interface
    Render all (or some) users retrieve from OpenStack Keystone server
    """

    c = get_keystone_client(request)
    #print(c.projects.create))
    all_users = c.projects.list()
    return render(request, "moon/projects.html", {"projects": all_users})

@login_required(login_url='/auth/login/')
def roles(request):
    """
    Users interface
    Render all (or some) users retrieve from OpenStack Keystone server
    """

    c = get_keystone_client(request)
    logger.debug(c.roles.list())
    all_users = c.roles.list()
    return render(request, "moon/roles.html", {"roles": all_users})
