# from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.http import HttpResponse
from moon.core.pdp import get_authz_manager
from moon.log_repository import get_log_manager
import hashlib
from moon import settings
# from moon.core.pap.core import PAP

import logging

logger = logging.getLogger(__name__)
LOGS = get_log_manager()

# TODO: this must be authenticated/secured!!!
# TODO: this must be CSRF protected!!!
@csrf_exempt
def tenants(request, id=None):
    response_data = {"auth": False}
    if request.method == 'POST':
        print("\033[32m"+str(request.POST)+"\033[m")
        crypt_key = hashlib.sha256()
        if "key" in request.POST:
            crypt_key.update(request.POST["key"])
            crypt_key.update(getattr(settings, "CNX_PASSWORD"))
            response_data["key"] = crypt_key.hexdigest()
        # print(pap.tenants.json())
        # response_data = json.dumps(pap.tenants.json())
        # try:
        manager = get_authz_manager()
        authz = manager.authz(
            subject=request.POST["Subject"],
            action=request.POST["Action"],
            object_name=request.POST["Object"],
            object_type=request.POST["ObjectType"],
            object_tenant=request.POST["Object_Tenant"],
            subject_tenant=request.POST["Subject_Tenant"]
        )
        tenant = request.POST.get("Subject_Tenant", "None")
        # TODO: need to check authorisation
        if not authz["auth"]:
            # print("\t\033[41m" + tenant_name + "/" + str(authz) + " for (" + "\033[m")
            log = "Unauthorized in tenant {tname} for ({subject} - {action} - {objecttype}/{object})".format(
                tname=authz["tenant_name"],
                authz=authz["auth"],
                subject=request.POST["Subject"],
                action=request.POST["Action"],
                object=request.POST["Object"],
                objecttype=request.POST["ObjectType"]
            )
            print("\t\033[41m"+log+"\033[m")
            LOGS.write(line=log)
        else:
            log = "Authorized in tenant {tname} for ({subject} - {action} - {objecttype}/{object})".format(
                tname=authz["tenant_name"],
                authz=authz["auth"],
                subject=request.POST["Subject"],
                action=request.POST["Action"],
                object=request.POST["Object"],
                objecttype=request.POST["ObjectType"]
            )
            print("\t\033[33m"+log+"\033[m")
            LOGS.write(line=log)

        # response_data["auth"] = authz
        if authz:
            response_data["auth"] = True
        # except Exception as e:
        #     logger.warning(e.message)
        #     logger.debug(e)
    return HttpResponse(json.dumps(response_data), content_type="application/json")