import json
from django.http import HttpResponse
from moon.core.pdp import get_intra_extensions, get_inter_extensions
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
                #  requesting_tenant and requested_tenant can not be None
                if post_request.POST["requesting_tenant"] == post_request.POST["requested_tenant"]:
                    _intra_manager = get_intra_extensions()
                    authz_response["authz"] = _intra_manager.authz(
                        subject=post_request.POST["subject"],
                        object=post_request.POST["object"],
                        action=post_request.POST["action"]
                    )
                else:
                    _inter_manager = get_inter_extensions()
                    authz_response["authz"] = _inter_manager.authz(
                        requesting_tenant=post_request.POST["requesting_tenant"],
                        requested_tenant=post_request.POST["requested_tenant"],
                        subject=post_request.POST["subject"],
                        object=post_request.POST["object"],
                        action=post_request.POST["action"]
                    )
            else:
                # raise Error Unknown Tenant
                pass
    except:
        import sys
        import traceback
        print(sys.exc_info())
        print(traceback.print_exc())
    return HttpResponse(json.dumps(authz_response), content_type="application/json")
