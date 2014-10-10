import json
from django.http import HttpResponse
from moon.core.pdp import get_intra_extensions, get_inter_extensions
import hashlib
from moon import settings


# TODO: this must be authenticated/secured!!!
# TODO: this must be CSRF protected!!!


def mrm_authz(request):
    response_data = {"authz": "KO"}
    try:
        if request.method == 'POST':
            crypt_key = hashlib.sha256()
            if "key" in request.POST:
                crypt_key.update(request.POST["key"])
                crypt_key.update(getattr(settings, "CNX_PASSWORD"))
                response_data["key"] = crypt_key.hexdigest()

            if request.POST["Requesting_Tenant"] == request.POST["Requested_Tenant"]:  # TODO to update in keystone_hook.py
                intra_manager = get_intra_extensions()
                authz = intra_manager.authz(
                    subject=request.POST["Subject"],
                    object=request.POST["Object"],
                    action=request.POST["Action"]
                )
            else:
                inter_manager = get_inter_extensions()
                authz = inter_manager.authz(
                    requesting_tenant=request.POST["Requesting_Tenant"],
                    requested_tenant=request.POST["Requested_Tenant"],
                    subject=request.POST["Subject"],
                    object=request.POST["Object"],
                    action=request.POST["Action"]
                )

            response_data["authz"] = authz
    except:
        import sys
        import traceback
        print(sys.exc_info())
        print(traceback.print_exc())
    return HttpResponse(json.dumps(response_data), content_type="application/json")
