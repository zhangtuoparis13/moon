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
        print(request.POST)
        # print(pap.tenants.json())
        # response_data = json.dumps(pap.tenants.json())
        try:
            manager = Manager()
            # TODO: need to check authorisation
            response_data["auth"] = True
        except Exception as e:
            logger.warning(e.message)
            logger.debug(e)
    return HttpResponse(json.dumps(response_data), content_type="application/json")