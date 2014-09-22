import logging
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from moon.core.pap import get_pap
from moon.gui.views import save_auth


logger = logging.getLogger("moon.django")
# LOGS = get_log_manager()


def send_json(data):
    try:
        # print(pap.get_subjects(extension_uuid=uuid, user_uuid=request.session['user_id']))
        return HttpResponse(json.dumps(data))
    except:
        import traceback
        print(traceback.print_exc())
        return HttpResponse(json.dumps({}))

##########################################################
# Functions for getting information about intra-extensions
##########################################################


@login_required(login_url='/auth/login/')
@save_auth
def intra_extensions(request, uuid=None):
    pap = get_pap()
    return send_json(pap.get_intra_extensions().keys())


@login_required(login_url='/auth/login/')
@save_auth
def intra_extension(request, uuid=None):
    pap = get_pap()
    extension = pap.get_intra_extensions()[uuid]
    return send_json(extension.get_data())


###############################################################
# Additional functions for getting information from Moon server
###############################################################


@login_required(login_url='/auth/login/')
@save_auth
def subjects(request, uuid=None):
    """
    Retrieve information about subjects from Moon server
    """
    pap = get_pap()
    return send_json({"subjects": list(
        pap.get_subjects(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


@login_required(login_url='/auth/login/')
@save_auth
def objects(request, uuid=None):
    """
    Retrieve information about objects from Moon server
    """
    pap = get_pap()
    return send_json({'objects': list(
        pap.get_objects(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


@login_required(login_url='/auth/login/')
@save_auth
def subject(request, uuid=None):
    """
    Retrieve information about subjects from Moon server
    """
    pap = get_pap()
    return send_json({"subjects": list(
        pap.get_subjects(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


@login_required(login_url='/auth/login/')
@save_auth
def object(request, uuid=None):
    """
    Retrieve information about objects from Moon server
    """
    pap = get_pap()
    return send_json({'objects': list(
        pap.get_objects(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


@login_required(login_url='/auth/login/')
@save_auth
def subject_categories(request, uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def object_categories(request, uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def subject_category(request, name=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def object_category(request, name=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def subject_category_values(request, uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def object_category_values(request, uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def subject_category_value(request, cat=None, value=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def object_category_value(request, cat=None, value=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def subject_assignments(request, uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def object_assignments(request, uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def subject_assignment(request, assign_uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def object_assignment(request, assign_uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def rules(request, uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def rule(request, rule_uuid=None):
    return send_json({})
