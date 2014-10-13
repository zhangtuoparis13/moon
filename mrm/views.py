import json
from django.http import HttpResponse
from moon.core.pdp import get_intra_extensions, get_inter_extensions
import hashlib
from moon import settings


# TODO: this must be authenticated/secured!!!
# TODO: this must be CSRF protected!!!


def mrm_authz(request):
    """
    post_data = [
        ('requesting_tenant', requesting_tenant_uuid),
        ('requested_tenant', requested_tenant_uuid),
        ('object', object_uuid),
        ('subject', subject_uuid),
        ('action', action),
        ('RAW_PATH_INFO', self._server_path),
        ('key', key)
    ]
    """

    response_data = {"authz": "KO"}
    try:
        if request.method == 'POST':
            crypt_key = hashlib.sha256()
            if "key" in request.POST:
                crypt_key.update(request.POST["key"])
                crypt_key.update(getattr(settings, "CNX_PASSWORD"))
                response_data["key"] = crypt_key.hexdigest()

            if request.POST["requesting_tenant"] and request.POST["requested_tenant"]:
                #  requesting_tenant and requested_tenant can not be None
                if request.POST["requesting_tenant"] == request.POST["requested_tenant"]:
                    _intra_manager = get_intra_extensions()
                    _authz_result = _intra_manager.authz(
                        subject=request.POST["subject"],
                        object=request.POST["object"],
                        action=request.POST["action"]
                    )
                else:
                    _inter_manager = get_inter_extensions()
                    _authz_result = _inter_manager.authz(
                        requesting_tenant=request.POST["requesting_tenant"],
                        requested_tenant=request.POST["requested_tenant"],
                        subject=request.POST["Subject"],
                        object=request.POST["Object"],
                        action=request.POST["Action"]
                    )
                response_data["authz"] = _authz_result
            else:
                # raise Error Unknown Tenant
                pass
    except:
        import sys
        import traceback
        print(sys.exc_info())
        print(traceback.print_exc())
    return HttpResponse(json.dumps(response_data), content_type="application/json")
