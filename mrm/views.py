# from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.http import HttpResponse
from moon.core.pdp import Manager
from moon.log_repository import LOGS
import hashlib
from moon import settings
# from moon.core.pap.core import PAP

import logging

logger = logging.getLogger(__name__)


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
        manager = Manager()
        authz, tenant_name = manager.authz(
            subject=request.POST["Subject"],
            action=request.POST["Action"],
            object_name=request.POST["Object"],
            object_tenant=request.POST["Object_Tenant"],
            subject_tenant=request.POST["Subject_Tenant"]
        )
        tenant = request.POST.get("Subject_Tenant", "None")
        # TODO: need to check authorisation
        if not authz:
            # print("\t\033[41m" + tenant_name + "/" + str(authz) + " for (" + "\033[m")
            log = "Unauthorized for {tname}/{authz} for ({subject} - {action} - {object})".format(
                tname=tenant_name,
                authz=authz,
                subject=request.POST["Subject"],
                action=request.POST["Action"],
                object=request.POST["Object"]
            )
            print("\t\033[41m"+log+"\033[m")
            LOGS.write(line=log)
        else:
            log = "Authorized for {tname}/{authz} for ({subject} - {action} - {object})".format(
                tname=tenant_name,
                authz=authz,
                subject=request.POST["Subject"],
                action=request.POST["Action"],
                object=request.POST["Object"]
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