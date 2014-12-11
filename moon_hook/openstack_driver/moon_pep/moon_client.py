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

import uuid
import hashlib
import urllib
import urllib2
import json
import re
import logging
import httplib


logger = logging.getLogger(__name__)


class MoonClient:

    def __init__(self, api_file="/etc/moon/api.json", managed_objects=list(("server", "servers", "action"))):
        self._api_json = json.loads(file(api_file).read())
        self._api_dict = {}
        for attr in self._api_json["attributes"]:
            if "server_id" in attr:
                self._api_dict[attr] = "(?P<server_id>[\w-]+)"
            elif "tenant_id" in attr:
                self._api_dict[attr] = "(?P<project_id>\w+)"
            elif "project_id" in attr:
                self._api_dict[attr] = "(?P<project_id>\w+)"
            # elif "id" in attr:
            #     self._api_dict[attr] = "(?P<id>\w{32})"
            else:
                self._api_dict[attr] = "(\w+)"
        for _request in self._api_json["data"]:
            # if _request["object"] not in managed_objects:
            #     self._api_json["data"].remove(_request)
            #     continue
            name = _request["name"]
            for key in self._api_dict:
                key = "{"+key+"}"
                name =   name.replace(key, "{_id}").replace("{_id}", key, 1)
            try:
                name = name.format(**self._api_dict)
            except:
                import traceback
                logger.error(name)
                logger.error(self._api_dict)
                logger.error(self._api_json["attributes"])
                logger.error(traceback.format_exc())
            _request[u"re"] = re.compile(name)
            _request[u"re_name"] = name

    def set_server(self, host, port, baseurl="mrm", path="", password=""):
        self._moon_server_host = host
        self._moon_server_port = port
        self._moon_server_baseurl = baseurl
        self._moon_server_url = "http://{host}:{port}/{baseurl}/authz".format(
            host=self._moon_server_host,
            port=self._moon_server_port,
            baseurl=self._moon_server_baseurl
        )
        self._moon_server_path = path
        self._moon_server_password = password

    def send_authz(self, authz):
        conn = httplib.HTTPConnection(self._moon_server_host, self._moon_server_port)
        method = "POST"
        url = "/{baseurl}/authz".format(baseurl=self._moon_server_baseurl)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
        }
        conn.request(method, url, json.dumps(authz), headers=headers)
        resp = conn.getresponse()
        content = resp.read()
        conn.close()
        try:
            return json.loads(content)
        except ValueError:
            return {"error": content}

    def authz(self, authz_request):
        """
        authz_request = {
            'requesting_tenant': requesting_tenant_uuid,
            'requested_tenant': requested_tenant_uuid,
            'subject': subject_uuid,
            'object': object_uuid,
            'action', action
        }
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
        authz_response2 = {
            'authz': "OK"/"KO",
            'message': "xxooxxoo"
        }
        """
        post_request = dict()
        post_request["requesting_tenant"] = authz_request["requesting_tenant"]
        post_request["requested_tenant"] = authz_request["requested_tenant"]
        post_request["subject"] = authz_request["subject"]
        post_request["object"] = authz_request["object"]
        post_request["action"] = authz_request["action"]
        key = str(uuid.uuid4())
        post_request["key"] = key

        try:
            # TODO: the connection must be secured!
            authz_response = self.send_authz(post_request)
            crypt_key = hashlib.sha256()
            crypt_key.update(key)
            crypt_key.update(self._moon_server_password)
            if "key" not in authz_response or authz_response["key"] != crypt_key.hexdigest():
                return {
                    "authz": "KO",
                    "message": "Connection problem with Moon MRM",
                    "detail": authz_response
                }
            else:
                authz_response.pop("key")
                authz_response["message"] = "Connection established with Moon MRM"
                return authz_response
        except Exception as e:
            # TODO: in production must raise an error and don't allow connection
            logger.warning("Exception occured " + str(e))

    def get_project(self, path):
        # logger.info("get_project " + path)
        try:
            if "/tenants" in path or "/projects" in path:
                return path.split('/')[2]
            elif len(path.strip("/").split("/")[0]) == 32:
                return path.strip("/").split("/")[0]
        except IndexError:
            return "NoTenant"

    def get_action(self, request_environ):
        # logger.warning(str(self._api_json["data"]))
        _action = ""
        _object_uuid = ""
        _object_type = ""
        _tenant_uuid = ""
        _method = request_environ['REQUEST_METHOD']
        path_info = request_environ['PATH_INFO']
        if re.search("^/v\d+/", request_environ['PATH_INFO']):
            path_info = request_environ['PATH_INFO'][request_environ['PATH_INFO'].index("/", 1):]
        try:
            _tenant_uuid = self.get_project(path_info)
        except IndexError:
            pass
        # _url = path_info.replace("-", "_")
        for _request in self._api_json["data"]:
            search = re.search(_request['re'], path_info)
            if _request['method'] == _method and search:
                _action = _request['action']
                _object_type = _request['object']
                _object_uuid = search.groupdict().get("server_id", "")
                # _object_uuid = _url.split("/")[-1]
                # if _object_type in ("server", "servers"):
                    # logger.warning("-------------------")
                    # logger.warning("path_info="+str(path_info))
                    # logger.warning("_request['re_name']="+str(_request['re_name']))
                    # logger.warning("_method="+str(_method))
                    # logger.warning("_request['desc']="+str(_request['desc']))
                    # logger.warning("_action="+str(_action))
                    # logger.warning("_object_type="+str(_object_type))
                    # logger.warning("_object_uuid="+str(_object_uuid))
                    # logger.warning("_tenant_uuid="+str(_tenant_uuid))
                    # logger.warning("search.groupdict()="+str(search.groupdict()))
                    # logger.warning("-------------------")
                # if _object_uuid in ("action", ):
                #     # BAD
                #     logger.warning("ACTION: {} {} {} {}".format(_action, _object_type, _object_uuid, _tenant_uuid))
                #     _object_uuid = _url.split("/")[-2]
                #     _object_type = "server"
                if len(_object_type) == 0:
                    continue
                return _action, _object_uuid, _object_type, _tenant_uuid
        return _action, _object_uuid, _object_type, _tenant_uuid

    def get_server_url(self):
        return self._moon_server_url


moon_client = MoonClient("/etc/moon/api.json")


def get_moon_client(host, port, baseurl="mrm", path="", password=""):
    moon_client.set_server(host, port, baseurl, path, password)
    return moon_client