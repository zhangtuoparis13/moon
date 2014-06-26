import os
import logging
from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import register
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from keystoneclient.v3 import client
from keystoneclient.v3.users import User
from keystoneclient.v3.projects import Project

from gi import settings
from moon.core.pap.core import PAP
from django.utils.safestring import mark_safe
# from moon.info_repository.driver_dispatcher import get_tables, get_elements, get_db_diag, get_attrs_list, get_element
from moon.core.pdp import get_admin_manager, get_authz_manager
from moon.log_repository import get_log_manager
from moon.core.pip import get_pip


logger = logging.getLogger("moon.django")
LOGS = get_log_manager()


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
def sync(request):
    """
    Interface of the application for syncing Moon database with Keystone and Nova databases
    """
    pip = get_pip()
    sync_results = pip.sync_db_with_keystone()
    sync_results = sync_results.replace("\n", "<br/>\n")
    sync_results = sync_results.replace("KO", "<span class=\"notauthorized\">Error</span>\n")
    sync_results = sync_results.replace("OK", "<span class=\"authorized\">OK</span>\n")
    return render(request, "moon/base_site.html", {"sync_results": mark_safe(sync_results)})


@login_required(login_url='/auth/login/')
def intra_extensions(request):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    pap = PAP(kclient=get_keystone_client(request))
    extensions = pap.admin_manager.get_intra_extensions()
    return render(request, "moon/intra-extensions.html", {
        "extensions": extensions
    })


@login_required(login_url='/auth/login/')
def intra_extension(request, id=None):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    pap = PAP(kclient=get_keystone_client(request))
    extension = pap.admin_manager.get_intra_extensions(uuid=id)
    return render(request, "moon/intra-extensions.html", {
        "extension": extension,
        "roles": pap.get_roles(extension_uuid=id),
        "groups": pap.get_groups(extension_uuid=id),
        "types": pap.get_object_attributes(extension_uuid=id, category="type"),
        "actions": pap.get_object_attributes(extension_uuid=id, category="action"),
        "securities": pap.get_object_attributes(extension_uuid=id, category="security"),
        "size": pap.get_object_attributes(extension_uuid=id, category="size"),
    })


@login_required(login_url='/auth/login/')
def inter_extensions(request):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    error = ""
    pap = PAP(kclient=get_keystone_client(request))
    if request.META['REQUEST_METHOD'] == "POST":
        post_args = request.POST
        requesting = post_args["requesting"]
        requested = post_args["requested"]
        type = post_args["type"]
        if requesting == requested:
            error = "Requesting tenant and requested are identical."
        else:
            pap.admin_manager.add_inter_extension(
                requesting=requesting,
                requested=requested,
                type=type
            )
    extensions = pap.admin_manager.get_inter_extensions()
    tenants = pap.admin_manager.get_tenant()
    subjects = pap.admin_manager.get_users(
        tenant_uuid=tenants[0].uuid
    )
    objects = pap.admin_manager.get_objects(
        tenant_uuid=tenants[1].uuid
    )
    return render(request, "moon/inter-extensions.html", {
        "extensions": extensions,
        "tenants": tenants,
        "selected_tenant1": tenants[0],
        "subjects": subjects,
        "selected_tenant2": tenants[1],
        "objects": objects,
        "error": error,
    })


@login_required(login_url='/auth/login/')
def inter_extension(request, id=None):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    error = ""
    pap = PAP(kclient=get_keystone_client(request))
    extension = pap.admin_manager.get_inter_extensions(uuid=id)[0]
    return render(request, "moon/inter-extensions.html", {
        "extension": extension,
        "tenants": pap.admin_manager.get_tenant(),
        "error": error,
    })


@register.filter
def get_log(dictionary, key):
    value = eval("dictionary.{}".format(key))
    return value


@register.filter
def get_tenant_name(uuid):
    pap = PAP()
    tenant = pap.admin_manager.get_tenant(tenant_uuid=uuid)[0]
    return tenant.name


@register.filter
def get_vent_name(uuid):
    pap = PAP()
    vent = pap.admin_manager.get_virtual_entity(uuid=uuid)[0]
    return vent.name


@register.filter
def get_vent_category_name(uuid):
    pap = PAP()
    vent = pap.admin_manager.get_virtual_entity(uuid=uuid)[0]
    return vent.name


@register.filter
def rule_length(dictionary):
    return len(dictionary["o_attr"])+len(dictionary["s_attr"])


@login_required(login_url='/auth/login/')
def logs_repository(request):
    """
    Log viewer interface
    """
    logs = LOGS.read(limit=30)
    logs.reverse()
    pap = PAP()
    for log in logs:
        if type(log.value) is dict:
            if log.value["object_tenant"] != "None":
                extension = pap.admin_manager.get_intra_extensions(tenant_uuid=log.value["object_tenant"])
                if extension:
                    log.value["subject"] = extension.get_subject(uuid=log.value["subject"])["name"]
                log.value["object_tenant"] = pap.admin_manager.get_tenant(
                    tenant_uuid=log.value["object_tenant"]
                )[0].name
            if log.value["subject_tenant"] != "None":
                extension = pap.admin_manager.get_intra_extensions(tenant_uuid=log.value["subject_tenant"])
                if extension:
                    try:
                        log.value["subject"] = extension.get_subject(uuid=log.value["subject"])["name"]
                    except TypeError, IndexError:
                        pass
                try:
                    log.value["subject_tenant"] = pap.admin_manager.get_tenant(
                        tenant_uuid=log.value["subject_tenant"]
                    )[0].name
                except AttributeError:
                    pass
            if log.value["auth"] is True:
                log.value["auth"] = "<span class=\"authorized\">Authorized</span>"
            elif log.value["auth"] is False:
                log.value["auth"] = "<span class=\"notauthorized\">Not Authorized</span>"
            else:
                log.value["auth"] = "<span class=\"outofscope\">{}</span>".format(log.value["auth"])
            html = """<b>{auth}/{rule_name}</b>
            <ul>
                <li><b>action:</b> {action}</li>
                <li><b>subject:</b> {subject_tenant}/{subject}</li>
                <li><b>object:</b> {object_tenant}/[{object_type}]{object_name}</li>
                <li><b>message:</b> {message}</li>
            </ul>
            """.format(**log.value)
            log.value = mark_safe(html)
    return render(request, "moon/logs.html", {
        "logs": logs,
        })
