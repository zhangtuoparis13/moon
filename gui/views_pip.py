import logging
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from moon.core.pip import get_pip
from moon.gui.views import save_auth
from django.views.decorators.csrf import csrf_protect, csrf_exempt


logger = logging.getLogger("moon.django")


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def projects(request, project_uuid=None):
    pip = get_pip()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        for key in ("name", "description", "enabled", "domain"):
            if key not in data.keys():
                return HttpResponse(json.dumps({"projects": list(pip.get_tenants(uuid=project_uuid))}))
        pip.add_tenant(data)
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pip.del_tenant(project_uuid)
    return HttpResponse(json.dumps({"projects": list(pip.get_tenants(uuid=project_uuid))}))


@login_required(login_url='/auth/login/')
@save_auth
def users(request, project_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps({"users": list(pip.get_subjects(tenant=project_uuid, user_uuid=user_uuid))}))


@login_required(login_url='/auth/login/')
@save_auth
def objects(request, project_uuid=None, object_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps({"objects": list(pip.get_objects(tenant=project_uuid, object_uuid=object_uuid))}))


@login_required(login_url='/auth/login/')
@save_auth
def roles(request, project_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps({"roles": list(pip.get_roles(project_uuid=project_uuid, user_uuid=user_uuid))}))


@login_required(login_url='/auth/login/')
@save_auth
def groups(request, project_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps({"groups": list(pip.get_groups(project_uuid=project_uuid, user_uuid=user_uuid))}))


@login_required(login_url='/auth/login/')
@save_auth
def role_assignments(request, project_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(
        {"role_assignments": list(pip.get_users_roles_assignment(project_uuid=project_uuid, user_uuid=user_uuid))}
    ))


@login_required(login_url='/auth/login/')
@save_auth
def group_assignments(request, project_uuid=None, user_uuid=None):
    pip = get_pip()
    return HttpResponse(json.dumps(
        {"group_assignments": list(pip.get_users_groups_assignment(project_uuid=project_uuid, user_uuid=user_uuid))}
    ))


@login_required(login_url='/auth/login/')
@save_auth
def images(request):
    pip = get_pip()
    return HttpResponse(json.dumps({"images": list(pip.get_images())}))


@login_required(login_url='/auth/login/')
@save_auth
def flavors(request):
    pip = get_pip()
    return HttpResponse(json.dumps({"flavors": list(pip.get_flavors())}))


