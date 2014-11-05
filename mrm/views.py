import json
from django.http import HttpResponse
from moon.core.pdp import pdp_authz
import hashlib
from moon import settings
from django.views.decorators.csrf import csrf_protect, csrf_exempt


# TODO: this must be authenticated/secured!!!
# TODO: this must be CSRF protected!!!


@csrf_exempt
def mrm_authz(post_request):
    """
    post_request = {
        'requesting_tenant': requesting_tenant_uuid,
        'requested_tenant': requested_tenant_uuid,
        'subject': subject_uuid,
        'object': object_uuid,
        'action', action,
        'key': key
    }
    authz_response = {
        'authz': "OK"/"KO",
        'key': key
    }
    """

    authz_response = {"authz": "KO"}
    try:
        if post_request.method == 'POST':
            data = json.loads(post_request.read())
            print("\033[32mrequest={}\033[m".format(data))
            if "key" in data:
                crypt_key = hashlib.sha256()
                crypt_key.update(data["key"])
                crypt_key.update(getattr(settings, "CNX_PASSWORD"))
                authz_response["key"] = crypt_key.hexdigest()
            if "requesting_tenant" in data and "requested_tenant" in data:
                authz_response["authz"] = pdp_authz(
                    data["subject"],
                    data["object"],
                    data["action"],
                    data["requesting_tenant"],
                    data["requested_tenant"]
                )
            else:
                authz_response["authz"] = pdp_authz(
                    data["subject"],
                    data["object"],
                    data["action"]
                )
    except:
        import sys
        import traceback
        print(sys.exc_info())
        print(traceback.print_exc())
        if getattr(settings, "DEBUG"):
            authz_response["error"] = traceback.format_exc()
    finally:
        if authz_response["authz"] == "OK":
            print("\033[43mresponse={}\033[m".format(authz_response))
        else:
            print("\033[41mresponse={}\033[m".format(authz_response))
        return HttpResponse(json.dumps(authz_response), content_type="application/json")
