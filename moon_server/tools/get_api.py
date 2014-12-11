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

from HTMLParser import HTMLParser
import urllib2
import re
import json
import sys

api_urls = (
    "http://developer.openstack.org/api-ref-blockstorage-v2.html",
    "http://developer.openstack.org/api-ref-blockstorage-v1.html",
    "http://developer.openstack.org/api-ref-compute-v2.html",
    "http://developer.openstack.org/api-ref-compute-v2-ext.html",
    "http://developer.openstack.org/api-ref-compute-v3.html",
    "http://developer.openstack.org/api-ref-databases-v1.html",
    "http://developer.openstack.org/api-ref-identity-v3.html",
    "http://developer.openstack.org/api-ref-identity-v2.html",
    "http://developer.openstack.org/api-ref-image-v2.html",
    "http://developer.openstack.org/api-ref-image-v1.html",
    "http://developer.openstack.org/api-ref-networking-v2.html",
    "http://developer.openstack.org/api-ref-objectstorage-v1.html",
    "http://developer.openstack.org/api-ref-orchestration-v1.html",
    "http://developer.openstack.org/api-ref-telemetry-v2.html"
)

objects = (
    ("tenant", "project"),
    "cloudpipe",
    "user",
    "interface",
    "aggregate",
    "agent",
    "quota",
    "limit",
    "image",
    "key",
    "flavor",
    "server",
    "network",
    "metadata",
    "volume",
    "token",
    "association",
    "extension",
    "event",
    "software",
    "resource",
    "container",
    "monitor",
    "metering-label",
    "router",
    ("floating-ip", "floatingip"),
    "subnet",
    "member",
    "tag",
    "group",
    "template",
    "endpoint",
    "service",
    "domain",
    "region",
    "extension",
    "policy",
    "consumer",
    "credentials",
    "database",
    "action",
    "hypervisor",
    "host",
    "migration",
    "keypair",
    "alarm",
    "pool",
    "vips",
    "port",
    "role",
    "meter",
    "assignment",
    "instance",
    ("audit-log", "audit", "log"),
    "cell"
)

methods = ("GET", "PUT", "TRACE", "DELETE", "HEAD", "PATCH", "OPTIONS", "CONNECT", "POST")

api_dict = {
    "data": [],
    "attributes": [],
    "objects": list(objects),
    "actions": map(lambda x: x.lower(), methods)
}

interfaces = []
cpt = 0

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    __all = {"method": "", "name": "", "desc": "", "action": "", "object": ""}
    __tag = ""
    __data = ""
    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag, attrs
        if tag.lower() == "span":
            for attr in attrs:
                if "class" == attr[0] and "label label-success" == attr[1]:
                    # print(tag, attrs)
                    self.__tag = tag
        elif tag.lower() == "div":
            for attr in attrs:
                if "class" == attr[0] and "col-md-5" == attr[1]:
                    # print(tag, attrs)
                    self.__tag = tag
        # else:
        #     self.__tag = ""
        #     self.__data = ""
    def handle_endtag(self, tag):
        global cpt
        # print "Encountered an end tag :", tag
        # print(self.__all)
        if len(self.__tag) > 0:
            # print(self.__tag, self.__data)
            if self.__tag == "span" and self.__data.upper() in methods:
                self.__all["method"] = self.__data.upper()
            elif self.__tag == "div" and self.__all["method"] != "":
                if self.__all["name"] == "":
                    self.__data = self.__data.replace("-", "_")
                    if self.__data[0] != "/":
                        self.__all["name"] = "/"+self.__data
                    else:
                        self.__all["name"] = self.__data
                elif self.__all["desc"] == "":
                    __tmp = self.__data.replace("\n", "").strip()
                    self.__all["desc"] = re.sub("\s+", " ", __tmp)
                    if self.__all["name"] not in interfaces:
                        for obj in objects:
                            for element in reversed(self.__all["name"].split("/")):
                                # sys.stderr.write("{}/{}\n".format(str(obj), str(type(obj))))
                                if type(obj) == str and obj in element.lower():
                                    self.__all["object"] = obj
                                    break
                                elif type(obj) in (list, tuple):
                                    # sys.stderr.write("{}/{}\n".format(str(obj), str(element)))
                                    for __obj in obj:
                                        if __obj in element.lower():
                                            self.__all["object"] = obj[0]
                        self.__all["action"] = self.__all["method"].lower()
                        api_dict["data"].append(dict(self.__all))
                        attrs = re.findall("\{(\w+)\}", self.__all["name"])
                        # sys.stderr.write("find {} in {}\n".format(attrs, self.__all["name"]))
                        for attr in attrs:
                            if attr not in api_dict["attributes"]:
                                api_dict["attributes"].append(attr)
                                # sys.stderr.write("  append {}\n".format(attr))
                        sys.stderr.write("\t{} -> {}\n".format(self.__all["object"].rjust(15), self.__all["name"]))
                        sys.stderr.flush()
                        interfaces.append(self.__all["name"])
                        cpt += 1
                    self.__all = {"method": "", "name": "", "desc": "", "action": "", "object": ""}
            self.__tag = ""
            self.__data = ""
    def handle_data(self, data):
        # print "Encountered some data  :", data
        if len(self.__tag) > 0:
            if len(data.strip()) > 0:
                self.__data += data

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

for url in api_urls:
    sys.stderr.write("\nFetching \033[32m{}\033[m\t".format(url))
    sys.stderr.flush()
    result = urllib2.urlopen(url)
    r = result.read()
    sys.stderr.write("OK\n")
    parser.feed(r)

#PATCH api because of errors:
api_dict["data"].append({
    "action": "post",
    "object": "token",
    "method": "POST",
    "name": "/v2.0/tokens",
    "desc": "set a token."
})

json_str = json.dumps(api_dict, indent=4)
# print(api_dict.keys())
sys.stderr.write("\nLength of string: {}\n".format(len(json_str)))
sys.stderr.write("\n{} interfaces fetched...\n".format(cpt))
sys.stderr.flush()

print(json_str)