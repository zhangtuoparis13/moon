import json
from django.http import HttpResponse
from moon.core.pdp import pdp_authz
import hashlib
from moon import settings


# TODO: this must be authenticated/secured!!!
# TODO: this must be CSRF protected!!!


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
            if "key" in post_request.POST:
                crypt_key = hashlib.sha256()
                crypt_key.update(post_request.POST["key"])
                crypt_key.update(getattr(settings, "CNX_PASSWORD"))
                authz_response["key"] = crypt_key.hexdigest()

            if post_request.POST["requesting_tenant"] and post_request.POST["requested_tenant"]:
                authz_response["authz"] = pdp_authz(
                    post_request.POST["subject"],
                    post_request.POST["object"],
                    post_request.POST["action"],
                    post_request.POST["requesting_tenant"],
                    post_request.POST["requested_tenant"]
                )
            else:
                authz_response["authz"] = pdp_authz(
                    post_request.POST["subject"],
                    post_request.POST["object"],
                    post_request.POST["action"]
                )
    except:
        import sys
        import traceback
        print(sys.exc_info())
        print(traceback.print_exc())
    return HttpResponse(json.dumps(authz_response), content_type="application/json")
