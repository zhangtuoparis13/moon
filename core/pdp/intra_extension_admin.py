from moon.core.pdp.extension import Extension


class AdminExtension(Extension):
    def authz(self, sub, obj, act):
        pass


'''
class AdminExtension(Extension):
    def authz(self, sub, obj, act):
        """Admin Authz interface
        """
        auth = {
            "auth": False,
            "rule_name": "None",
            "message": "",
            "subject": user_uuid,
            "action": "action-write" if mode == "w" else "action-read",
            "object_name": obj,
            "tenant_name": tenant["name"],
            "extension_name": ext.get_name(),
        }
        if "objects" not in self.__administration:
            auth["message"] = "No administration protocol for extension"
            auth["auth"] = True
            return auth
        if self.__tenant["name"] != auth["tenant_name"]:
            auth["message"] = "Tenant not found."
            return auth
        if auth["subject"] not in map(lambda x: x["uuid"], self.__subjects):
            auth["message"] = "User not found."
            return auth
        if auth["object_name"] not in map(lambda x: x["name"], self.__administration["objects"]):
            auth["message"] = "Object not found."
            return auth
        for obj in self.__administration["objects"]:
            if obj["name"] == auth["object_name"]:
                auth["object_uuid"] = obj["uuid"]
                break
        for rule in self.__administration["rules"]:
            _auth = False
            for s_rule in rule["s_attr"]:
                data = self.__subjectsAssignments
                attribute = s_rule["value"]
                for sbj in data:
                    if type(attribute) not in (list, tuple):
                        attribute = [attribute, ]
                    for att in attribute:
                        if auth["subject"] == sbj["subject"] and att in sbj["attributes"]:
                            _auth = True
                            break
            if not _auth:
                auth["message"] = "Rules on subject don't match."
                continue
            for o_rule in rule["o_attr"]:
                    if o_rule["category"] == "action":
                        _auth = self.__has_admin_assignment(
                            object_uuid=auth["object_uuid"],
                            attribute_uuid=auth["action"])
                        if not _auth:
                            auth["message"] = "Rules on action assignments don't match."
                            break
                        if auth["action"] not in o_rule["value"]:
                            auth["message"] = "Rules on action don't match."
                            break
                    else:
                        _auth = self.__has_admin_assignment(
                            object_uuid=auth["object_uuid"],
                            attribute_uuid=o_rule["value"])
                        if not _auth:
                            auth["message"] = "Rules on object don't match."
                            print(auth["object_uuid"], o_rule["value"])
                            break
            else:
                auth["message"] = ""
                auth["auth"] = True
                break
        # auth = ext.authz(auth=auth)
        # print("\033[32min wrapped\033[m")
        # try:
        #     auth = ext.authz(auth=auth)
        #     print(auth)
        #     print("\033[32m----------------------------------------\033[m")
        # except:
        #     import sys
        #     print("\033[31mException\033[m", sys.exc_info())
        # print("\t-> {subject} {action} {object_name} {auth}: {message}".format(**auth))
        if auth["auth"] is not True:
            print("\033[31mCalling {} for {}/{} on {}/{}\033[m".format(
                function.__name__,
                tenant["name"],
                user_uuid,
                obj,
                mode))
            raise AdminException(auth["message"])
'''