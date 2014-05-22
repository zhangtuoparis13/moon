from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import register
import os
import logging
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from keystoneclient.v3 import client
from keystoneclient.v3.users import User
from keystoneclient.v3.projects import Project
from gi import settings
from core.pap.core import PAP
from moon.info_repository.driver_dispatcher import get_tables, get_elements, get_db_diag, get_attrs_list, get_element

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


class TablesSelectForm(forms.Form):
    """
    Definition of the form which allow the selection a a child for a tenant
    """
    main_tables = forms.ChoiceField()
    assignment_tables = forms.ChoiceField()

    def __init__(self, tables=(), query=None, attrs=None):
        tables = map(lambda x: (str(x), str(x)), tables)
        super(TablesSelectForm, self).__init__(query)
        main_tables = filter(lambda x: "assignment" not in x[0].lower(), tables)
        main_tables.insert(0, ("", ""))
        assignment_tables = filter(lambda x: "assignment" in x[0].lower(), tables)
        assignment_tables.insert(0, ("", ""))
        self.fields['main_tables'].choices = main_tables
        self.fields['assignment_tables'].choices = assignment_tables


def add_element(table, columns, request, kclient=None):
    """Add an element to the database
    """
    pap = PAP(kclient=kclient)
    attributes = {}
    for column in columns:
        if column in request:
            attributes[column] = request[column]
    pap.add_element(table=table, attributes=attributes)


def delete_element(table, columns, uuid, kclient=None):
    """Add an element to the database
    """
    pap = PAP(kclient=kclient)
    attributes = dict()
    attributes["uuid"] = uuid
    pap.delete_element(table=table, attributes=attributes)


@register.filter
def get_item(dictionary, key):
    value = ""
    table = key.split("_")[0].title()
    value = eval("dictionary.{}".format(key))
    if "tenant_uuid" in key:
        pap = PAP()
        if value:
            value = pap.tenants.get_tenant(uuid=value).name
    elif "_uuid" in key:
        element = get_element(type=table, attributes={"uuid": value})
        value = element[0].name
    return value



@register.filter
def get_widget(column, value=None):
    column = conditional_escape(column)
    if value:
        value = eval("value.{}".format(column))
    html = """<input type="text" name="{}"/>""".format(column)
    html_value = """<input type="text" name="{}" value="{}"/>""".format(column, value)
    radio = """
<label for="{column}_true" value="True">True:</label>
<input type="radio" id="{column}_true" name="{column}" checked/>
<label for="{column}_false" value="False">False:</label>
<input type="radio" id="{column}_false" name="{column}"/>""".format(column=column)
    select = """
<select id="{column}_id" name="{column}">
{options}
</select>
    """
    options = """<option value="{uuid}">{val}</option>"""
    options_selected = """<option value="{uuid}" selected>{val}</option>"""
    static = """<label>{value}</label><input type="hidden" name="{column}" value="{value}"/>""".format(
        column=column,
        value=value)
    if "enabled" in column:
        return mark_safe(radio)
    elif "tenant_uuid" in column:
        pap = PAP()
        tenants = map(lambda x: (x.uuid, x.name), pap.tenants.list())
        all_options = []
        for element in tenants:
            if value and value == element[0]:
                all_options.append(options_selected.format(uuid=element[0], val=element[1]))
            else:
                all_options.append(options.format(uuid=element[0], val=element[1]))
        return mark_safe(select.format(column=column, options=all_options))
    elif "_uuid" in column:
        table = column.split("_")[0].title()
        pap = PAP()
        elements = get_elements(type=table)
        elements = map(lambda x: (x.uuid, x.name), elements)
        all_options = []
        for element in elements:
            if value and value == element[0]:
                all_options.append(options_selected.format(uuid=element[0], val=element[1]))
            else:
                all_options.append(options.format(uuid=element[0], val=element[1]))
        return mark_safe(select.format(column=column, options=all_options))
    elif column in ("id", "uuid"):
        return mark_safe(static)
    else:
        if value:
            return mark_safe(html_value)
        else:
            return mark_safe(html)


@login_required(login_url='/auth/login/')
def userdb(request):
    """
    User DB administration interface
    """
    c = get_keystone_client(request)
    tables = TablesSelectForm(tables=get_tables())
    elements = []
    columns = None
    selected_table = None
    uuid_column_number = 0
    edit_uuid = None
    addcolumns = ()
    if request.method == 'GET':
        # print("GET")
        # print(request.GET)
        if "edit" in request.GET:
            edit_uuid = request.GET.get('uuid')
        elif "delete" in request.GET:
            delete_element(table=request.GET.get('table'),
                           columns=get_attrs_list(request.GET.get('table')),
                           uuid=request.GET.get("uuid"),
                           kclient=c)
        selected_table = request.GET.get('table')
        if selected_table:
            elements = get_elements(type=selected_table)
            addcolumns = filter(lambda x: x not in ("id", "uuid"), get_attrs_list(selected_table))
            columns = get_attrs_list(selected_table)
    elif request.method == 'POST':
        # print("POST")
        # print(request.POST)
        action = request.POST.get("action")
        submit = request.POST.get("submit") or ""
        if action == "add" or submit.lower() == "update":
            add_element(table=request.POST['selected_table'],
                        columns=get_attrs_list(request.POST['selected_table']),
                        request=request.POST,
                        kclient=c)
        form = TablesSelectForm(query=request.POST, tables=get_tables())
        if form.is_valid():
            __table = form.cleaned_data['tables']
            selected_table = __table
            __elements = get_elements(type=__table)
            elements = __elements
            columns = get_attrs_list(__table)
        if "selected_table" in request.POST and not selected_table == 0:
            selected_table = request.POST['selected_table']
            if len(elements) == 0:
                elements = get_elements(type=selected_table)
                columns = get_attrs_list(selected_table)
        if selected_table:
            addcolumns = filter(lambda x: x not in ("id", "uuid"), get_attrs_list(selected_table))
    graph = get_db_diag()
    return render(request, "moon/userdb.html", {
        "tables": tables,
        "selected_table": selected_table,
        "elements": elements,
        "columns": columns,
        "addcolumns": addcolumns,
        "uuid_column_number": uuid_column_number,
        "edit_uuid": edit_uuid,
        "graph": graph})
