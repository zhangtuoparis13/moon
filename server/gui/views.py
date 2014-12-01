import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import register
from keystoneclient.v3 import client
from moon import settings
from django.utils.safestring import mark_safe
from keystoneclient import exceptions
import json
from django.http import HttpResponse
# from moon.log_repository import get_log_manager
from moon.core.pip import get_pip
from moon.core.pap import get_pap


logger = logging.getLogger("moon.django")
# LOGS = get_log_manager()


def save_auth(function):
    def wrapped(*args, **kwargs):
        #FIXME: what happen if 2 different users use the application at the same time
        try:
            get_pip().set_creds_from_token(args[0].session["token"])
        except KeyError:
            # No token so not authenticated
            pass
        except exceptions.Unauthorized:
            # Token is not valid, user must re-authenticate
            pass
        # try:
        #     username = args[0].session['user_id']
        #     globals()["username"] = username
        # except AttributeError:
        #     username = globals().get("username")
        # except IndexError:
        #     username = globals().get("username")
        # except KeyError:
        #     #When authenticating, username is not set
        #     username = ""
        # print("\033[32mCalling {}({})\033[m".format(function.__name__, username))
        result = None
        # try:
        result = function(*args, **kwargs)
        # except:
        #     import traceback
        #     print("\033[41mException in "+__name__)
        #     print(traceback.print_exc())
        #     print("\033[m")
        function.__globals__["username"] = None
        #FIXME must unset creds but it brokes JSON interface
        # get_pip().unset_creds()
        return result
    return wrapped


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


########################################################
# Specific functions for GUI module
########################################################


@save_auth
@login_required(login_url='/auth/login/')
def index(request):
    """
    Front interface of the application
    """
    return render(request, "moon/index.html")


@save_auth
@login_required(login_url='/auth/login/')
def sync(request, uuid=None):
    """
    Interface of the application for syncing Moon database with Keystone and Nova databases
    """
    pap = get_pap()
    sync_results = pap.sync_db_with_keystone(tenant_uuid=uuid)
    sync_results = sync_results.replace("\n", "<br/>\n")
    sync_results = sync_results.replace("KO", "<span class=\"notauthorized\">Error</span>\n")
    sync_results = sync_results.replace("OK", "<span class=\"authorized\">OK</span>\n")
    return render(request, "moon/index.html", {"sync_results": mark_safe(sync_results)})

@save_auth
@login_required(login_url='/auth/login/')
def tenants(request, uuid=None):
    """
    Interface of the application for syncing Moon database with Keystone and Nova databases
    """
    pap = get_pap()
    t = pap.get_tenants(uuid=uuid)
    return render(request, "moon/tenants.html", {"tenants": t})


@save_auth
@login_required(login_url='/auth/login/')
def intra_extensions(request):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    pap = get_pap()
    extensions = pap.get_intra_extensions().values()
    return render(request, "moon/intra-extensions.html", {
        "extensions": extensions
    })


@login_required(login_url='/auth/login/')
@save_auth
def intra_extension(request, uuid=None):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        if "rules_list" in request.POST:
            name = request.POST.get("name", "NO-NAME")
            description = request.POST.get("description", "")
            rules_str = request.POST.get("rules_list", "")
            # rule = dict()
            # rule["name"] = name
            # rule["description"] = description
            # rule["s_attr"] = []
            # rule["o_attr"] = []
            s_attr = []
            o_attr = []
            for line in rules_str.splitlines():
                try:
                    _type, _category, _value = line.strip().split(":")
                    if _type == "subject":
                        s_attr.append({"category": _category, "value": _value})
                    elif _type == "object":
                        o_attr.append({"category": _category, "value": _value})
                except:
                    import sys
                    print("Exception in view", sys.exc_info())
                    continue
            # rule["s_attr"] = s_attr
            # rule["o_attr"] = o_attr
            extension = pap.get_intra_extensions(uuid=uuid)[0]
            extension.add_rule(
                name=name,
                description=description,
                subject_attrs=s_attr,
                object_attrs=o_attr
            )
    extension = {}
    subjects = None
    objects = None
    rules = None
    try:
        print("looking for extention {}".format(uuid))
        extension = pap.get_intra_extensions(uuid=uuid)
        print(extension)
        subjects = pap.get_subjects(extension_uuid=uuid, user_uuid=request.session['user_id'])
        print(subjects)
        objects = pap.get_objects(extension_uuid=uuid, user_uuid=request.session['user_id'])
        print(objects)
        rules = pap.get_rules(extension_uuid=uuid, user_uuid=request.session['user_id'])
        print(rules)
    except IndexError:
        pass
    except TypeError:
        pass
    return render(request, "moon/intra-extensions.html", {
        "extension": extension,
        "sujects": subjects,
        "objects": objects,
        "rules": rules,
    })


@login_required(login_url='/auth/login/')
@save_auth
def inter_extensions(request):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    error = ""
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        post_args = request.POST
        requesting = post_args["requesting"]
        requested = post_args["requested"]
        type = post_args["type"]
        _objects = []
        _subjects = []
        for key in post_args.keys():
            if "object" in key:
                _objects.append(post_args[key])
            elif "subject" in key:
                _subjects.append(post_args[key])
        if requesting == requested:
            error = "Requesting tenant and requested are identical."
        else:
            pap.add_inter_extension(
                requesting=requesting,
                requested=requested,
                connexion_type=type,
                requesting_subjects=_subjects,
                requested_objects=_objects
            )
    extensions = pap.get_inter_extensions()
    tenants = pap.get_tenant()
    # subjects = pap.admin_manager.get_users(
    #     tenant_uuid=tenants[0].uuid
    # )
    # objects = pap.admin_manager.get_objects(
    #     tenant_uuid=tenants[1].uuid
    # )
    return render(request, "moon/inter-extensions.html", {
        "extensions": extensions,
        "tenants": tenants,
        # "selected_tenant1": tenants[0],
        # "subjects": subjects,
        # "selected_tenant2": tenants[0],
        # "objects": objects,
        "error": error,
    })


@login_required(login_url='/auth/login/')
@save_auth
def inter_extension(request, uuid=None):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    error = ""
    pap = get_pap()
    extension = pap.get_inter_extensions(uuid=id)[0]
    if request.META['REQUEST_METHOD'] == "DELETE":
        #TODO: check if deletion is OK
        pap.delete_inter_extension(uuid=uuid)
        return HttpResponse(json.dumps({'delete': True}))
        # return render(request, "moon/inter-extensions.html", {
        #     "extensions": pap.admin_manager.get_inter_extensions(),
        #     "tenants": pap.admin_manager.get_tenant(),
        #     "error": error,
        # })
    return render(request, "moon/inter-extensions.html", {
        "extension": extension,
        "tenants": pap.get_tenant(),
        "error": error,
    })


@login_required(login_url='/auth/login/')
@save_auth
def intra_extension_attributes(request, uuid=None, type=None):
    """
    User interface
    Render one user retrieve from OpenStack Keystone server
    """
    error = ""
    pap = get_pap()
    attributes = []
    if type.lower() == "subject":
        attributes = list(pap.get_subject_attributes(extension_uuid=uuid))
    elif type.lower() == "object":
        attributes = list(pap.get_object_attributes(extension_uuid=uuid))
    categories = list(set(map(lambda x: x["category"], attributes)))
    return HttpResponse(json.dumps({'attributes': attributes, "categories": list(categories)}))


@register.filter
def get_log(dictionary, key):
    value = eval("dictionary.{}".format(key))
    return value


@register.filter
def get_tenant_name(uuid):
    pap = get_pap()
    tenant = pap.get_tenant(uuid=uuid)[0]
    return tenant.name


@register.filter
def get_vent_name(uuid):
    pap = get_pap()
    vent = pap.get_virtual_entity(uuid=uuid)[0]
    return vent.name


@register.filter
def get_vent_category_name(uuid):
    pap = get_pap()
    vent = pap.get_virtual_entity(uuid=uuid)[0]
    return vent.name


@register.filter
def rule_length(dictionary):
    return len(dictionary["o_rules"])+len(dictionary["s_rules"])


@register.filter
def is_managed(tenant):
    pap = get_pap()
    if pap.get_intra_extensions(uuid=tenant["uuid"]):
        return True
    else:
        return False


@login_required(login_url='/auth/login/')
@save_auth
def logs_repository(request):
    """
    Log viewer interface
    """
    return render(request   )
    # logs = LOGS.read(limit=30)
    # logs.reverse()
    # pap = get_pap()
    # for log in logs:
    #     if type(log.value) is dict:
    #         if log.value["object_tenant"] != "None":
    #             extension = pap.get_intra_extensions(tenant_uuid=log.value["object_tenant"])
    #             if extension:
    #                 log.value["subject"] = extension.get_subject(uuid=log.value["subject"])["name"]
    #             try:
    #                 log.value["object_tenant"] = pap.get_tenant(
    #                     tenant_uuid=log.value["object_tenant"]
    #                 )[0].name
    #             except IndexError:
    #                 pass
    #         if log.value["subject_tenant"] != "None":
    #             extension = pap.get_intra_extensions(tenant_uuid=log.value["subject_tenant"])
    #             if extension:
    #                 try:
    #                     log.value["subject"] = extension.get_subject(uuid=log.value["subject"])["name"]
    #                 except TypeError:
    #                     pass
    #                 except IndexError:
    #                     pass
    #             try:
    #                 log.value["subject_tenant"] = pap.get_tenant(
    #                     tenant_uuid=log.value["subject_tenant"]
    #                 )[0].name
    #             except AttributeError:
    #                 pass
    #             except IndexError:
    #                 # Tenant does not exist anymore
    #                 pass
    #         if log.value["auth"] is True:
    #             log.value["auth"] = "<span class=\"authorized\">Authorized</span>"
    #         elif log.value["auth"] is False:
    #             log.value["auth"] = "<span class=\"notauthorized\">Not Authorized</span>"
    #         else:
    #             log.value["auth"] = "<span class=\"outofscope\">{}</span>".format(log.value["auth"])
    #         html = """<b>{auth}/{rule_name}</b>
    #         <ul>
    #             <li><b>action:</b> {action}</li>
    #             <li><b>subject:</b> {subject_tenant}/{subject}</li>
    #             <li><b>object:</b> {object_tenant}/[{object_type}]{object_name}</li>
    #             <li><b>message:</b> {message}</li>
    #         </ul>
    #         """.format(**log.value)
    #         log.value = mark_safe(html)
    # return render(request, "moon/logs.html", {
    #     "logs": logs,
    # })


# @login_required(login_url='/auth/login/')
# @save_auth
# def get_tenants(request, **kwargs):
#     pap = get_pap()
#     pip = get_pip()
#     tenants = pip.get_tenants(pap=pap)
#     return render(request, "moon/tenants.html", {
#         "tenants": tenants
#     })


# @login_required(login_url='/auth/login/')
# @save_auth
# def get_tenant(request, id=None, **kwargs):
#     return render(request, "moon/tenants.html", {})


@register.filter
def has_subject_attribute(tenant, object_uuid=None):
    pap = get_pap()
    ext = pap.get_intra_extensions(tenant_uuid=tenant["uuid"])
    return ext.has_subject_attributes(uuid=object_uuid)


@login_required(login_url='/auth/login/')
@save_auth
def roles(request, uuid=None):
    """
    Users interface
    Render all roles retrieve from OpenStack Keystone server
    """
    pap = get_pap()
    if request.META['REQUEST_METHOD'] == "POST":
        tenants = []
        for key in request.POST:
            if len(key) == 32 and request.POST[key] == "on":
                tenants.append(key)
        pap.create_roles(name=request.POST["name"], description=request.POST["description"], tenants=tenants)
    elif request.META['REQUEST_METHOD'] == "DELETE":
        #TODO: check if deletion is OK
        pap.delete_roles(uuid=uuid)
        return HttpResponse(json.dumps({'delete': True}))
    #TODO add selection by tenant
    tenant = list(pap.get_tenants(name="admin"))[0]
    _roles = list(pap.get_roles(tenant=tenant))
    return render(request, "moon/roles.html", {
        "roles": _roles,
        "tenants": list(pap.get_tenants())
    })


# @login_required(login_url='/auth/login/')
# @save_auth
# def authz(request, id=None):
#     """
#     Internal authorisation interface
#     """
#     pap = get_pap()
#     # pip = get_pip()
#     return render(request, "moon/internal_authz.html", {
#     })