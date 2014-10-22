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
    if type(data) in (str, unicode):
        _data = re.findall("[\w\s\-_]", data)
        return "".join(_data).strip()
    return data


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


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def intra_extensions(request, uuid=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "policymodel" in data:
            uuid = pap.install_intra_extension_from_json(
                user_id=request.session['user_id'],
                extension_setting_name=data["policymodel"])
            return send_json({
                "intra_extensions":
                    pap.get_intra_extensions(user_id=request.session['user_id'])[uuid].get_data()
            })
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.delete_intra_extension(user_id=request.session['user_id'], intra_extension_uuid=uuid)
    elif uuid:
        extension = pap.get_intra_extensions(user_id=request.session['user_id'])[uuid]
        return send_json({"intra_extensions": extension.get_data()})
    return send_json({
        "intra_extensions":
            pap.get_intra_extensions(user_id=request.session['user_id']).keys()
    })


@login_required(login_url='/auth/login/')
@save_auth
def tenant(request, uuid=None):
    pap = get_pap()
    extension = pap.get_intra_extensions()[uuid]
    return send_json({"tenant": extension.get_tenant_uuid()})


@login_required(login_url='/auth/login/')
@save_auth
def policies(request):
    pap = get_pap()
    return send_json({"policies": pap.get_policies()})


#####################################################
# Functions for getting information about subjects
#####################################################


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def subjects(request, uuid=None, subject_id=None):
    """
    Retrieve information about subjects from Moon server
    """
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "name" in data and "password" in data:
            uuid = pap.add_subject(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                subject=data)
            return send_json({"subjects": list(
                pap.get_subjects(extension_uuid=uuid, user_uuid=request.session['user_id'])[uuid]
            )})
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


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def objects(request, uuid=None, object_id=None):
    """
    Retrieve information about objects from Moon server
    """
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "object" in data:
            uuid = pap.add_object(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                object=data["object"])
            if uuid:
                return send_json({
                    "objects": pap.get_objects(extension_uuid=uuid, user_uuid=request.session['user_id'])[uuid]
                })
            else:
                return send_json({"objects": list()})
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


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def subject_categories(request, uuid=None, category_id=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "category_id" in data:
            uuid = pap.add_subject_category(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(data["category_id"]))
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


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def object_categories(request, uuid=None, category_id=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "category_id" in data:
            pap.add_object_category(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(data["category_id"]))
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


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def subject_category_values(request, uuid=None, category_id=None, value=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "category_id" in data and "value" in data:
            pap.add_subject_category_value(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(data["category_id"]),
                category_value=filter_input(data["value"]))
            category_id = filter_input(data["category_id"])
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


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def object_category_values(request, uuid=None, category_id=None, value=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "category_id" in data and "value" in data:
            pap.add_object_category_value(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(data["category_id"]),
                category_value=filter_input(data["value"]))
            category_id = filter_input(data["value"])
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


######################################################################
# Functions for getting information about assignments
######################################################################


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def subject_assignments(request, uuid=None, category_id=None, subject_id=None, value=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "category_id" in data and "subject_id" in data and "value" in data:
            pap.add_subject_assignment(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(data["category_id"]),
                subject_id=filter_input(data["subject_id"]),
                category_value=filter_input(data["value"]))
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
def object_assignments(request, uuid=None, category_id=None, object_id=None, value=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "category_id" in data and "object_id" in data and "value" in data:
            pap.add_object_assignment(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                category_id=filter_input(data["category_id"]),
                object_id=filter_input(data["object_id"]),
                category_value=filter_input(data["value"]))
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


######################################################################
# Functions for getting information about rules
######################################################################


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def rules(request, uuid=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        if "sub_cat_value" in data and "obj_cat_value" in data:
            pap.add_rule(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                sub_cat_value=filter_input(data["sub_cat_value"]),
                obj_cat_value=filter_input(data["obj_cat_value"]))
    elif request.META['REQUEST_METHOD'] == "DELETE":
        data = json.loads(request.read())
        if "sub_cat_value" in data and "obj_cat_value" in data:
            pap.del_rule(
                extension_uuid=uuid,
                user_uuid=request.session['user_id'],
                sub_cat_value=filter_input(data["sub_cat_value"]),
                obj_cat_value=filter_input(data["obj_cat_value"]))
    # return send_json({"rules": list(
    #     pap.get_rules(extension_uuid=uuid, user_uuid=request.session['user_id'])
    # )})
    return send_json(
        {"rules": pap.get_rules(extension_uuid=uuid, user_uuid=request.session['user_id'])}
    )


######################################################################
# Functions for getting information about Inter-Extensions
######################################################################


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def inter_extensions(request, uuid=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        data = json.loads(request.read())
        for key in [
            u'requested_intra_extension_uuid',
            u'requesting_intra_extension_uuid',
            u'obj_list',
            u'act',
            u'genre',
            u'sub_list'
        ]:
            if key not in data:
                return send_json({"inter_extensions": list(
                    pap.get_installed_inter_extensions(extension_uuid=uuid, user_id=request.session['user_id'])
                )})
        inter_extension_uuid, vent_uuid = pap.create_collaboration(
            user_id=request.session['user_id'],
            requesting_intra_extension_uuid=data["requesting_intra_extension_uuid"],
            requested_intra_extension_uuid=data["requested_intra_extension_uuid"],
            genre=data["genre"],
            sub_list=data["sub_list"],
            obj_list=data["obj_list"],
            act=data["act"]
        )
        return send_json({
            "inter_extensions": map(
                lambda x: x.get_data(),
                pap.get_installed_inter_extensions(extension_uuid=uuid, user_id=request.session['user_id'])
            ),
            "uuid": inter_extension_uuid,
            "vents": vent_uuid
        })
    elif request.META['REQUEST_METHOD'] == "DELETE":
        data = json.loads(request.read())
        for key in [
            u'genre',
            u'vents',
        ]:
            if key not in data:
                return send_json({"inter_extensions": list(
                    pap.get_installed_inter_extensions(extension_uuid=uuid, user_id=request.session['user_id'])
                )})
        pap.destroy_collaboration(
            user_id=request.session['user_id'],
            genre=data["genre"],
            inter_extension_uuid=uuid,
            vent_uuid=data["vents"])
    return send_json({"inter_extensions": map(
        lambda x: x.get_data(),
        pap.get_installed_inter_extensions(extension_uuid=uuid, user_id=request.session['user_id'])
    )})


######################################################################
# Functions for getting information about Inter-Extensions
######################################################################


@csrf_exempt
@login_required(login_url='/auth/login/')
@save_auth
def super_extensions(request, tenant_uuid=None, intra_extension_uuid=None):
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        # data = json.loads(request.read())
        pap.create_mapping(
            user_id=request.session['user_id'],
            tenant_uuid=filter_input(tenant_uuid),
            intra_extension_uuid=filter_input(intra_extension_uuid))
    elif request.META['REQUEST_METHOD'] == "DELETE":
        pap.destroy_mapping(
            user_id=request.session['user_id'],
            tenant_uuid=filter_input(tenant_uuid),
            intra_extension_uuid=filter_input(intra_extension_uuid))
    return send_json({"super_extensions": list(
        pap.list_mappings(user_id=request.session['user_id'])
    )})
