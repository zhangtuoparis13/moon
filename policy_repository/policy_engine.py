import json
import re
# Default rules for testing
RULES = (
    (
        ('s_attrs', 'role', "admin"),
        ('s_attrs', 'group', "group1"),
        ('o_attrs', 'type', "vm")
    ),
    (
        ('s_attrs', 'role', "admin"),
        ('s_attrs', 'group', "group2"),
        ('o_attrs', 'type', "vm")
    ),
)


ATTRS = {
    's_attrs': {            # user = "Ruan", "Thomas"
        'role': (),         # "admin"
        'group': ()         # "group1"
    },
    'o_attrs': {            # "vm", "logfiles", "nas"
        'type': (),         # "compute", "log", "storage", "network"
        'size': (),         # "small", "medium", "big"
        'security': ()      # "public", "private", "confidential"
    },
    'a_attrs': {            # "admin", "access"
        'activity': (),     # "manage", "use"
        'security': (),     # "normal", "ssl"
    },
}


class PolicyPlugin:
    def __init__(self, filename=""):
        try:
            tables = json.loads(open(filename).read())
        except IOError:
            raise Exception("[{}] Unable to read file {}".format(__name__, filename))
        # parse file

        # self.rules = ()
        self.rules = tables["RULES"]

        # self.attributes = {'s_attrs': {}, 'a_attrs': {}, 'o_attrs': {}, 'other_attrs':{}}
        self.attributes = tables["METADATA"]

        self.pointer = self

    def authz(self, subject=None, action=None, object_name=None, attributes=None):
        authz = [False, False, False]
        debug_str = ""
        debug_str += "s_attrs:\033[31m{s_attrs}\033[m\n" \
                     "o_attrs:\033[31m{o_attrs}\033[m\n" \
                     "a_attrs:\033[31m{a_attrs}\033[m\n".format(
                     **attributes
                     )
        rules = self.rules.keys()
        rules.sort()
        for rule in rules:
            table, value = self.rules[rule]["s_attrs"]
            # print("#"*40, attributes["s_attrs"])
            if (not subject or subject == "None") and \
               (table == "Role" or table == "Subject") and \
               value == "*":
                authz[0] = True
            for element in attributes["s_attrs"]:
                # print("-"*20)
                # print(table, value)
                # print(element.__class__, element.name)
                # print(re.match(element.name, value))
                # print(element.__tablename__, table)
                # print("-"*20)
                if element.__tablename__ == table and re.match(element.name, value):
                    authz[0] = True
                    break
            table, value = self.rules[rule]["o_attrs"]
            for element in attributes["o_attrs"]:
                # print(attributes["o_attrs"])
                # print(re.match(element.name, value))
                # print(element.__tablename__, table)
                if element.__tablename__ == table and re.match(element.name, value):
                    authz[1] = True
                    break
            table, value = self.rules[rule]["a_attrs"]
            for element in attributes["a_attrs"]:
                # print(rule, attributes["o_attrs"])
                # print(rule, re.match(element.name, value))
                # print(rule, element.__tablename__, table)
                if element.__tablename__ == table and re.match(element.name, value):
                    authz[2] = True
                    break
            debug_str += "self.rules[rule]=\033[32m" + str(self.rules[rule])+"\033[m\n"
            debug_str += "authz=\033[33m" + str(authz) + "\033[m\n"
            if authz == [True, True, True]:
                return rule
        # print(debug_str)
        return False


def load_policy_plugin(filename=""):
    pp = PolicyPlugin(filename=filename)
    return pp.pointer, pp.attributes