import logging
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from moon.core.pap import get_pap
from moon.gui.views import save_auth
import re


logger = logging.getLogger("moon.django")
# LOGS = get_log_manager()


def filter_input(data):
    _data = re.findall("[\w\s\-_]", data)
    return "".join(_data).strip()


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


#####################################################
# Functions for getting information about subjects
#####################################################


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


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def subject(request, uuid=None, subject_id=None):
    """
    Retrieve information about subjects from Moon server
    """
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "subject_uuid" in request.POST:
            pap.add_subject(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                subject_id=filter_input(request.POST["subject_uuid"]))
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.del_subject(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            subject_id=filter_input(subject_id))
    return send_json({"subjects": list(
        pap.get_subjects(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


#####################################################
# Functions for getting information about objects
#####################################################


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


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def object(request, uuid=None, object_id=None):
    """
    Retrieve information about objects from Moon server
    """
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "object_uuid" in request.POST:
            pap.add_object(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                object_id=filter_input(request.POST["object_uuid"]))
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.del_object(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            object_id=filter_input(object_id))
    return send_json({"objects": list(
        pap.get_objects(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


###############################################################
# Functions for getting information about subject categories
###############################################################


@login_required(login_url='/auth/login/')
@save_auth
def subject_categories(request, uuid=None):
    pap = get_pap()
    return send_json({"subject_categories": list(
        pap.get_subject_categories(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def subject_category(request, uuid=None, category_id=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "category_id" in request.POST:
            pap.add_subject_category(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(request.POST["category_id"]))
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.del_subject_category(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=filter_input(category_id))
    return send_json({"subject_categories": list(
        pap.get_subject_categories(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})

###############################################################
# Functions for getting information about object categories
###############################################################


@login_required(login_url='/auth/login/')
@save_auth
def object_categories(request, uuid=None):
    pap = get_pap()
    return send_json({"object_categories": list(
        pap.get_object_categories(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def object_category(request, uuid=None, category_id=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "category_id" in request.POST:
            pap.add_object_category(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(request.POST["category_id"]))
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.del_object_category(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=filter_input(category_id))
    return send_json({"object_categories": list(
        pap.get_object_categories(extension_uuid=uuid, user_uuid=request.session['user_id'])
    )})


######################################################################
# Functions for getting information about subject categories values
######################################################################


@login_required(login_url='/auth/login/')
@save_auth
def subject_category_values(request, uuid=None):
    pap = get_pap()
    results = dict()
    for cat in pap.get_subject_categories(extension_uuid=uuid, user_uuid=request.session['user_id']):
        results[cat] = list(pap.get_subject_category_values(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=cat
        ))
    return send_json({"subject_category_values": results})


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def subject_category_value(request, uuid=None, category_id=None, value=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "category_id" in request.POST and "value" in request.POST:
            pap.add_subject_category_value(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(request.POST["category_id"]),
                category_value=filter_input(request.POST["value"]))
            category_id = filter_input(request.POST["category_id"])
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.del_subject_category_value(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=filter_input(category_id),
            category_value=filter_input(value))
    results = dict()
    for cat in pap.get_subject_categories(extension_uuid=uuid, user_uuid=request.session['user_id']):
        results[cat] = list(pap.get_subject_category_values(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=cat
        ))
    return send_json({"subject_category_values": results})


######################################################################
# Functions for getting information about subject categories values
######################################################################


@login_required(login_url='/auth/login/')
@save_auth
def object_category_values(request, uuid=None):
    pap = get_pap()
    results = dict()
    for cat in pap.get_object_categories(extension_uuid=uuid, user_uuid=request.session['user_id']):
        results[cat] = list(pap.get_object_category_values(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=cat
        ))
    return send_json({"object_category_values": results})


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def object_category_value(request, uuid=None, category_id=None, value=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "category_id" in request.POST and "value" in request.POST:
            pap.add_object_category_value(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(request.POST["category_id"]),
                category_value=filter_input(request.POST["value"]))
            category_id = filter_input(request.POST["value"])
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.del_object_category_value(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=filter_input(category_id),
            category_value=filter_input(value))
    results = dict()
    for cat in pap.get_object_categories(extension_uuid=uuid, user_uuid=request.session['user_id']):
        results[cat] = list(pap.get_object_category_values(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=cat
        ))
    return send_json({"object_category_values": results})


@login_required(login_url='/auth/login/')
@save_auth
def subject_assignments(request, uuid=None):
    pap = get_pap()
    results = dict()
    for cat in pap.get_subject_categories(extension_uuid=uuid, user_uuid=request.session['user_id']):
        results[cat] = pap.get_subject_assignments(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=cat
        )
    return send_json({"subject_assignments": results})


@login_required(login_url='/auth/login/')
@save_auth
def object_assignments(request, uuid=None):
    pap = get_pap()
    results = dict()
    for cat in pap.get_object_categories(extension_uuid=uuid, user_uuid=request.session['user_id']):
        results[cat] = pap.get_object_assignments(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=cat
        )
    return send_json({"object_assignments": results})


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def subject_assignment(request, uuid=None, category_id=None, subject_id=None, value=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "category_id" in request.POST and "subject_id" in request.POST and "value" in request.POST:
            pap.add_subject_assignment(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(request.POST["category_id"]),
                subject_id=filter_input(request.POST["subject_id"]),
                category_value=filter_input(request.POST["value"]))
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.del_subject_assignment(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=filter_input(category_id),
            subject_id=filter_input(subject_id),
            category_value=filter_input(value))
    results = dict()
    for cat in pap.get_subject_categories(extension_uuid=uuid, user_uuid=request.session['user_id']):
        results[cat] = pap.get_subject_assignments(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=cat
        )
    return send_json({"subject_assignments": results})


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def object_assignment(request, uuid=None, category_id=None, object_id=None, value=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "category_id" in request.POST and "object_id" in request.POST and "value" in request.POST:
            pap.add_object_assignment(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(request.POST["category_id"]),
                object_id=filter_input(request.POST["object_id"]),
                category_value=filter_input(request.POST["value"]))
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.del_object_assignment(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=filter_input(category_id),
            object_id=filter_input(object_id),
            category_value=filter_input(value))
    results = dict()
    for cat in pap.get_object_categories(extension_uuid=uuid, user_uuid=request.session['user_id']):
        results[cat] = pap.get_object_assignments(
            extension_uuid=uuid,
            user_uuid=request.session['user_id'],
            category_id=cat
        )
    return send_json({"object_assignments": results})


@login_required(login_url='/auth/login/')
@save_auth
def rules(request, uuid=None):
    return send_json({})


@login_required(login_url='/auth/login/')
@save_auth
def rule(request, rule_uuid=None):
    return send_json({})
