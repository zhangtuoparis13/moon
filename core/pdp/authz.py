# from moon.core.pdp.core import get_internal_authz
#
# authz_manager = get_internal_authz()


def enforce(objs, mode="r"):
    if type(objs) not in (tuple, list):
        objs = [objs,]

    def enforce_decorator(function):
        def wrapped(*args, **kwargs):
            # tenant = dir(locals().get("args"))
            init_flag = globals().get("initialization")
            auth_flag = globals().get("authorisation")
            readonly_flag = globals().get("readonly")
            if not init_flag and not auth_flag and not readonly_flag:
                try:
                    ext = locals().get("args")[0]
                    toggle_auth_flag()
                    tenant = ext.get_tenant()
                    toggle_auth_flag()
                except IndexError:
                    raise Exception("Unable to get extension for authentication...")
                except AttributeError:
                    raise Exception("Unable to get tenant for authentication...")
                # username = locals().get("kwargs").get("username")
                user_uuid = globals().get("username")
                if not user_uuid:
                    raise Exception("Unable to authenticate connection...")
                for obj in objs:
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
                    auth = ext.authz(auth=auth)
                    # print("\t-> {subject} {action} {object_name} {auth}: {message}".format(**auth))
                    if auth["auth"] is not True:
                        print("\033[31mCalling {} for {}/{} on {}/{}\033[m".format(
                            function.__name__,
                            tenant["name"],
                            user_uuid,
                            obj,
                            mode))
                        raise Exception(auth["message"])
            result = None
            if readonly_flag and mode != "r":
                raise Exception("Read only mode set and write access required!")
            return function(*args, **kwargs)
        return wrapped
    return enforce_decorator


def translate_auth(function):
    def wrapped(*args, **kwargs):
        # username = globals().get("username")
        username = locals().get("username")
        # print(locals())
        try:
            username = args[0].session['user_id']
            # function.__globals__["username"] = username
            # globals()["username"] = username
            # locals()["username"] = username
            # setattr(function, "username", username)
        except AttributeError:
            username = locals().get("username")
            print("\tAttributeError", locals())
            # username = globals().get("username")
        except IndexError:
            username = locals().get("kwargs").get("username")
            print("\tIndexError", locals())
            # username = globals().get("username")
        # if not username:
        #     request = args[0]
        #     print(get_user(request))
        #     if request.user.is_authenticated():
        #         username = request.user.username
        #         print("\033[44mfound {}\033[m".format(username))
        # # setattr(function, "username", username)
        # # function.__globals__["username"] = username
        # globals()["username"] = username
        # print(globals().get("username"))
        print("\033[32mCalling {}({})\033[m".format(function.__name__, username))
        kwargs["username"] = username
        result = function(*args, **kwargs)
        function.__globals__["username"] = None
        return result
    return wrapped


def save_auth(function):
    def wrapped(*args, **kwargs):
        #FIXME: what happen if 2 different users use the application at the same time
        try:
            username = args[0].session['user_id']
            globals()["username"] = username
        except AttributeError:
            username = globals().get("username")
        except IndexError:
            username = globals().get("username")
        # print("\033[32mCalling {}({})\033[m".format(function.__name__, username))
        result = function(*args, **kwargs)
        function.__globals__["username"] = None
        return result
    return wrapped


def toggle_init_flag():
    if "initialization" not in globals():
        globals()["initialization"] = True
    else:
        globals()["initialization"] = not globals()["initialization"]


def toggle_readonly_flag():
    if "readonly" not in globals():
        globals()["readonly"] = True
    else:
        globals()["readonly"] = not globals()["readonly"]


def toggle_auth_flag():
    if "authorisation" not in globals():
        globals()["authorisation"] = True
    else:
        globals()["authorisation"] = not globals()["authorisation"]