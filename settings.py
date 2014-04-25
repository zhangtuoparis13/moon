
DATABASES = {
    'user_db': {
        'ENGINE': 'moon.info_repository.mysql_driver',
        'NAME': "user_db",
        'USER': "moonuser",
        'PASSWORD': "set a password here",
        'HOST': "",
        'PORT': ""
    },
    'tenant_db': {
        'ENGINE': 'moon.tenant_repository.mysql_driver',
        'NAME': "tenant_db",
        'USER': "moonuser",
        'PASSWORD': "set a password here",
        'HOST': "",
        'PORT': ""
    }
}

OPENSTACK_KEYSTONE_URL = "http://openstackserver:5000/v3"

INITIAL_DB = {
    # Subject attributes
    'Subject': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "password", "type": "String", "length": 254},
                {'name': "mail", "type": "String", "length": 254},
                {'name': "description", "type": "String", "length": 254},
                {'name': "domain", "type": "String", "length": 254},
                {'name': "project", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrKey",
        'description': "A user in the system.",
    },
    'Role': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "tenant_uuid", "type": "String", "length": 32},
                {'name': "description", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrValue",
        'description': "A role taken by a user.",
    },
    'Group': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "tenant_uuid", "type": "String", "length": 32},
                {'name': "description", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrValue",
        'description': "A group of users.",
    },
    'SubjectRoleAssignment': {
        'attributes': (
                {'name': "subject_uuid", "type": "String", "length": 32},
                {'name': "role_uuid", "type": "String", "length": 32},
                ),
        'type': "AttrValue",
        'description': "Mapping between User and role.",
    },
    'SubjectGroupAssignment': {
        'attributes': (
                {'name': "subject_uuid", "type": "String", "length": 32},
                {'name': "group_uuid", "type": "String", "length": 32},
                ),
        'type': "AttrValue",
        'description': "Mapping between User and Group.",
    },
    # Object attributes
    'Object': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "description", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrKey",
        'description': "A possible Object in the system.",
    },
    'Type': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "description", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrValue",
        'description': "A type of possible Object in the system.",
    },
    'Size': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "value", "type": "String", "length": 32},
                {'name': "unit", "type": "String", "length": 32},
                {'name': "description", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrValue",
        'description': "Size of a storage or of a network connection.",
    },
    'ObjectTypeAssignment': {
        'attributes': (
                {'name': "action_uuid", "type": "String", "length": 32},
                {'name': "type_uuid", "type": "String", "length": 32},
                ),
        'type': "AttrValue",
        'description': "Mapping between Object and Type.",
    },
    'ObjectSizeAssignment': {
        'attributes': (
                {'name': "action_uuid", "type": "String", "length": 32},
                {'name': "size_uuid", "type": "String", "length": 32},
                ),
        'type': "AttrValue",
        'description': "Mapping between Object and Size.",
    },
    # Action attributes
    'Action': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "description", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrKey",
        'description': "A possible Action in the system.",
    },
    'Activity': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "description", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrValue",
        'description': "A type/activity of possible Action in the system.",
    },
    'Security': {
        'attributes': (
                {'name': "uuid", "type": "String", "length": 32},
                {'name': "name", "type": "String", "length": 254},
                {'name': "value", "type": "String", "length": 32},
                {'name': "unit", "type": "String", "length": 32},
                {'name': "description", "type": "String", "length": 254},
                {'name': "enabled", "type": "Boolean"},
                ),
        'type': "AttrValue",
        'description': "Size of a storage or of a network connection.",
    },
    'ActionActivityAssignment': {
        'attributes': (
                {'name': "action_uuid", "type": "String", "length": 32},
                {'name': "type_uuid", "type": "String", "length": 32},
                ),
        'type': "AttrValue",
        'description': "Mapping between Action and Activity.",
    },
    'ActionSecurityAssignment': {
        'attributes': (
                {'name': "action_uuid", "type": "String", "length": 32},
                {'name': "size_uuid", "type": "String", "length": 32},
                ),
        'type': "AttrValue",
        'description': "Mapping between Action and Security.",
    },
}
