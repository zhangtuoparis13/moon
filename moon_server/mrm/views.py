# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
from django.http import HttpResponse
from moon_server.core.pdp import pdp_authz
import hashlib
from moon_server import settings
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from moon_server.tools.log.core import get_authz_logger

# TODO: this must be authenticated/secured!!!
# TODO: this must be CSRF protected!!!

authz_logger = get_authz_logger()

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
            authz_logger.info("request={}".format(data))
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
        authz_logger.critical(sys.exc_info())
        authz_logger.critical(traceback.print_exc())
        if getattr(settings, "DEBUG"):
            authz_response["error"] = traceback.format_exc()
    finally:
        if authz_response["authz"] == "OK":
            authz_logger.info("response={}".format(authz_response))
        elif authz_response["authz"] == "NoExtension":
            authz_logger.warning("response={}".format(authz_response))
        else:
            authz_logger.error("response={}".format(authz_response))
        return HttpResponse(json.dumps(authz_response), content_type="application/json")
