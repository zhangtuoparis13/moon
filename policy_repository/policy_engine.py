import json
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
        # check attr_values against self.rules
        pass


def load_policy_plugin(filename=""):
    pp = PolicyPlugin(filename=filename)
    return pp.pointer, pp.attributes