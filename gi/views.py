from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import logging
from keystoneclient.v3 import client
from keystoneclient.v3.users import User
from keystoneclient.v3.projects import Project
from gi import settings
from core.pap.core import PAP

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
    user_obj = pap.users.get_user(uuid=id)
    return render(request, "moon/users.html", {"user": user_obj})


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


class TenantChildAddForm(forms.Form):
    """
    Definition of the form which allow the selection a a child for a tenant
    """
    projects = forms.ChoiceField()

    def __init__(self, tenants=(), query=None):
        tenants = map(lambda x: (str(x.uuid), str(x.name)), tenants)
        print(tenants)
        super(TenantChildAddForm, self).__init__(query)
        self.fields['projects'].choices = tenants


class TenantAddForm(forms.Form):
    name = forms.CharField(max_length=100)
    domain = forms.CharField(max_length=100, initial="Default")
    description = forms.CharField(max_length=100, required=False)
    enable = forms.BooleanField(initial=True)


def draw_tenant_tree(tenants=(), selected_tenant_uuid=None):
    """
    Draw the tenant hierarchy in a svg file (in the static directory) and return the filename
    """
    filename = "tenants.svg"
    static_dir = getattr(settings, 'STATICFILES_DIRS', "")[0]
    import pygraphviz as pgv
    graph = pgv.AGraph(directed=True)
    __tmp_dic = {}
    for tenant in tenants:
        if tenant.uuid == selected_tenant_uuid:
            graph.add_node(tenant.name, color='red')
        else:
            graph.add_node(tenant.name)
        __tmp_dic[tenant.uuid] = tenant.name
    for tenant in tenants:
        for child in tenant.children:
            graph.add_edge(tenant.name, __tmp_dic[child])
    graph.draw(os.path.join(static_dir, filename), format="svg", prog="dot")
    return filename


@login_required(login_url='/auth/login/')
def projects(request):
    """
    Users interface
    Render all (or some) users retrieve from OpenStack Keystone server
    """
    pap = PAP(kclient=get_keystone_client(request))
    form = TenantAddForm()
    if request.method == 'POST':
        form = TenantAddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            domain = form.cleaned_data['domain']
            description = form.cleaned_data['description']
            enable = form.cleaned_data['enable']
            result = pap.tenants.create(
                name=name,
                domain=domain,
                description=description,
                enabled=enable
            )
            if type(result) is Project:
                result = "Project Created"
        else:
            raise forms.ValidationError("Form is not complete.")
    all_projects = pap.tenants.list() #get_projects()
    svg_graph = draw_tenant_tree(tenants=all_projects)
    return render(request, "moon/projects.html", {
        "projects": all_projects,
        "graph": svg_graph,
        "tenantform": form})


@login_required(login_url='/auth/login/')
def project(request, id=None):
    """
    project interface
    Render one user retrieve from Tenant Repositery
    """
    pap = PAP(kclient=get_keystone_client(request))
    # projects = pap.tenants.list() #get_projects()
    form = TenantChildAddForm(tenants=pap.tenants.list())
    if request.method == 'POST':
        form = TenantChildAddForm(query=request.POST, tenants=pap.tenants.list())
        if form.is_valid():
            __projects = form.cleaned_data['projects']
            if "Add" in request.POST.keys():
                pap.tenants.set_tenant_relationship(tenant_up=id, tenant_bottom=__projects)
            elif "Delete" in request.POST.keys():
                pap.tenants.unset_tenant_relationship(tenant_up=id, tenant_bottom=__projects)
        else:
            raise forms.ValidationError("Form is not complete.")
    project = pap.tenants.get_tenant(uuid=id)
    svg_graph = draw_tenant_tree(tenants=pap.tenants.list(), selected_tenant_uuid=id)
    return render(request, "moon/projects.html", {
        "project": project,
        "projects": projects,
        "form": form,
        "graph": svg_graph})


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
