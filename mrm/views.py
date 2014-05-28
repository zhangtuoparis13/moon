from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.http import HttpResponse
from moon.core.pdp import Manager
# from moon.core.pap.core import PAP

import logging

logger = logging.getLogger(__name__)


# TODO: this must be authenticated!!!
# TODO: this must be CSRF protected!!!
@csrf_exempt
def tenants(request, id=None):
    response_data = {"auth": False}
    if request.method == 'POST':
        print("\033[32m"+str(request.POST)+"\033[m")
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
            print("\t\033[41m" + tenant_name + "/" + str(authz) + "\033[m")
        else:
            print("\t\033[33m" + tenant_name + "/" + str(authz) + "\033[m")
        # response_data["auth"] = authz
        if authz:
            response_data["auth"] = True
        # except Exception as e:
        #     logger.warning(e.message)
        #     logger.debug(e)
    return HttpResponse(json.dumps(response_data), content_type="application/json")