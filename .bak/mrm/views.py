# from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.http import HttpResponse
from moon.core.pdp import get_intra_extensions
# from moon.log_repository import get_log_manager
import hashlib
from moon import settings
import logging


logger = logging.getLogger(__name__)
# LOGS = get_log_manager()

# TODO: this must be authenticated/secured!!!
# TODO: this must be CSRF protected!!!
@csrf_exempt
def tenants(request):
    response_data = {"auth": False}
    try:
        if request.method == 'POST':
            # print("\033[32m"+str(request.POST)+"\033[m")
            logger.info("request: " + request.POST["RAW_PATH_INFO"])
            crypt_key = hashlib.sha256()
            if "key" in request.POST:
                crypt_key.update(request.POST["key"])
                crypt_key.update(getattr(settings, "CNX_PASSWORD"))
                response_data["key"] = crypt_key.hexdigest()
            # print(pap.tenants.json())
            # response_data = json.dumps(pap.tenants.json())
            # try:
            manager = get_intra_extensions()
            authz = manager.authz(
                subject=request.POST["Subject"],
                action=request.POST["Action"],
                object_name=request.POST["Object"],
                object_type=request.POST["ObjectType"],
                object_tenant=request.POST["Object_Tenant"],
                subject_tenant=request.POST["Subject_Tenant"]
            )
            tenant = request.POST.get("Subject_Tenant", "None")
            args = {
                "tname": authz["tenant_name"],
                "authz": authz["auth"],
                "subject": request.POST["Subject"],
                "action": request.POST["Action"],
                "object": request.POST["Object"],
                "objecttype": request.POST["ObjectType"],
                "message": authz["message"],
            }
            if authz["auth"] == True:
                log = "{color}Authorized{endcolor} in tenant {tname} " \
                      "for ({subject} - {action} - {objecttype}/{object}) \n{message}"
                print(log.format(color="\033[33m", endcolor="\033[m", **args))
                # LOGS.write(line=log.format(color="", endcolor="", **args))
                # LOGS.write(authz)
            elif not authz["auth"]:
                log = "{color}Unauthorized{endcolor} in tenant {tname} " \
                      "for ({subject} - {action} - {objecttype}/{object}) \n{message}"
                print(log.format(color="\033[41m", endcolor="\033[m", **args))
                # LOGS.write(line=log.format(color="", endcolor="", **args))
                # LOGS.write(authz)
            else:
                # print("\t\033[41m" + tenant_name + "/" + str(authz) + " for (" + "\033[m")
                log = "{color}Out of Scope{endcolor} in tenant {tname} " \
                      "for ({subject} - {action} - {objecttype}/{object}) \n{message}"
                print(log.format(color="\033[42m", endcolor="\033[m", **args))
                # LOGS.write(line=log.format(color="", endcolor="", **args))
                # LOGS.write(authz)

            response_data["auth"] = authz
    except:
        import sys
        import traceback
        print(sys.exc_info())
        print(traceback.print_exc())
    return HttpResponse(json.dumps(response_data), content_type="application/json")
