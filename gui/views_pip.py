import logging
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from moon.core.pip import get_pip
from moon.gui.views import save_auth


logger = logging.getLogger("moon.django")


@login_required(login_url='/auth/login/')
@save_auth
def tenants(request, tenant_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(list(pip.get_tenants(uuid=tenant_uuid))))


@login_required(login_url='/auth/login/')
@save_auth
def subjects(request, tenant_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(list(pip.get_subjects(tenant=tenant_uuid))))


@login_required(login_url='/auth/login/')
@save_auth
def objects(request, tenant_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(list(pip.get_objects(tenant=tenant_uuid))))


@login_required(login_url='/auth/login/')
@save_auth
def roles(request, tenant_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(list(pip.get_roles(tenant_uuid=tenant_uuid, uuid=user_uuid))))


@login_required(login_url='/auth/login/')
@save_auth
def groups(request, tenant_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(list(pip.get_groups(tenant_uuid=tenant_uuid, uuid=user_uuid))))


@login_required(login_url='/auth/login/')
@save_auth
def role_assignments(request, tenant_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(list(pip.get_users_roles_assignment(tenant_uuid=tenant_uuid, users=(user_uuid,)))))


@login_required(login_url='/auth/login/')
@save_auth
def group_assignments(request, tenant_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(list(pip.get_users_groups_assignment(tenant_uuid=tenant_uuid, users=(user_uuid,)))))
