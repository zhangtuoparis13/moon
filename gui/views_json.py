import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import register
from keystoneclient.v3 import client
from moon.gui import settings
from django.utils.safestring import mark_safe
from keystoneclient import exceptions
import json
from django.http import HttpResponse
from moon.log_repository import get_log_manager
from moon.core.pip import get_pip
from moon.core.pap import get_pap
from moon.gui.views import save_auth


logger = logging.getLogger("moon.django")
LOGS = get_log_manager()


@login_required(login_url='/auth/login/')
@save_auth
def intra_extensions(request, uuid=None):
    pap = get_pap()
    return HttpResponse(json.dumps(pap.get_intra_extensions().keys()))


@login_required(login_url='/auth/login/')
@save_auth
def intra_extension(request, uuid=None):
    pap = get_pap()
    extension = pap.get_intra_extensions()[uuid]
    try:
        return HttpResponse(json.dumps(extension.get_data()))
    except:
        import traceback
        print(traceback.print_exc())
        return HttpResponse(json.dumps({}))

########################################################
# Functions for getting information from Keystone server
########################################################


@login_required(login_url='/auth/login/')
@save_auth
def get_tenants(request, uuid=None):
    """
    Retrieve information about tenants from Keystone server
    """
    pap = get_pap()
    return HttpResponse(json.dumps(list(pap.get_tenants(uuid=uuid))))


###############################################################
# Additional functions for getting information from Moon server
###############################################################


@login_required(login_url='/auth/login/')
@save_auth
def get_subjects(request, uuid=None):
    """
    Retrieve information about subjects from Moon server
    """
    print("-------------------------------------")
    pap = get_pap()
    try:
        print(pap.get_subjects(extension_uuid=uuid, user_uuid=request.session['user_id']))
        return HttpResponse(json.dumps({"subjects": list(
            pap.get_subjects(extension_uuid=uuid, user_uuid=request.session['user_id'])
        )}))
    except:
        import traceback
        print(traceback.print_exc())
        return HttpResponse(json.dumps({}))


@login_required(login_url='/auth/login/')
@save_auth
def get_objects(request, uuid=None):
    """
    Retrieve information about objects from Moon server
    """
    print("get_objects")
    pap = get_pap()
    try:
        print(pap.get_objects(extension_uuid=uuid, user_uuid=request.session['user_id']))
        return HttpResponse(json.dumps({'objects': list(
            pap.get_objects(extension_uuid=uuid, user_uuid=request.session['user_id'])
        )}))
    except:
        import traceback
        print(traceback.print_exc())
        return HttpResponse(json.dumps({}))


