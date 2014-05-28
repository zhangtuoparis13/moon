
DATABASES = {
    'user_db': {
        'ENGINE': 'moon.info_repository.mysql_driver',
        'NAME': "user_db",
        'USER': "moonuser",
        'PASSWORD': "P4ssw0rd",
        'HOST': "127.0.0.1",
        'PORT': "3306"
    },
    'tenant_db': {
        'ENGINE': 'moon.tenant_repository.shelve_driver',
        'NAME': "/etc/moon/tenant.db",
        'USER': "",
        'PASSWORD': "",
        'HOST': "",
        'PORT': ""
    }
}

POLICY_PLUGIN_TABLE = "/etc/moon/policy_tables.json"

OPENSTACK_KEYSTONE_URL = "http://openstackserver:5000/v3"

OPENSTACK_API = "/etc/moon/api.json"

INITIAL_DB = {
    # Subject attributes
    'Subject': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "password", "type": "String", "parameters": [254, ]},
                {'name': "mail", "type": "String", "parameters": [254, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "domain", "type": "String", "parameters": [254, ]},
                {'name': "project", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrKey",
        'description': "A user in the system.",
    },
    'Role': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "tenant_uuid", "type": "String", "parameters": [32, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrValue",
        'description': "A role taken by a user.",
    },
    'Group': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "tenant_uuid", "type": "String", "parameters": [254, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrValue",
        'description': "A group of users.",
    },
    'SubjectRoleAssignment': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "subject_uuid", "type": "ForeignKey", "parameters": ['Subject.uuid', ]},
                {'name': "role_uuid", "type": "ForeignKey", "parameters": ['Role.uuid', ]},
                {'name': "tenant_uuid", "type": "String", "parameters": [32, ]},
        ),
        'type': "AttrValue",
        'description': "Mapping between User and role.",
    },
    'SubjectGroupAssignment': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "subject_uuid", "type": "ForeignKey", "parameters": ['Subject.uuid', ]},
                {'name': "group_uuid", "type": "ForeignKey", "parameters": ['Group.uuid', ]},
                {'name': "tenant_uuid", "type": "String", "parameters": [32, ]},
        ),
        'type': "AttrValue",
        'description': "Mapping between User and Group.",
    },
    # Object attributes
    'Object': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrKey",
        'description': "A possible Object in the system.",
    },
    'Type': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrValue",
        'description': "A type of possible Object in the system.",
    },
    'Size': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "value", "type": "String", "parameters": [32, ]},
                {'name': "unit", "type": "String", "parameters": [32, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrValue",
        'description': "Size of a storage or of a network connection.",
    },
    'ObjectTypeAssignment': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "object_uuid", "type": "ForeignKey", "parameters": ['Object.uuid', ]},
                {'name': "type_uuid", "type": "ForeignKey", "parameters": ['Type.uuid', ]},
        ),
        'type': "AttrValue",
        'description': "Mapping between Object and Type.",
    },
    'ObjectSizeAssignment': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "object_uuid", "type": "ForeignKey", "parameters": ['Object.uuid', ]},
                {'name': "size_uuid", "type": "ForeignKey", "parameters": ['Size.uuid', ]},
        ),
        'type': "AttrValue",
        'description': "Mapping between Object and Size.",
    },
    # Action attributes
    'Action': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrKey",
        'description': "A possible Action in the system.",
    },
    'Activity': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrValue",
        'description': "A type/activity of possible Action in the system.",
    },
    'Security': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "name", "type": "String", "parameters": [254, ]},
                {'name': "value", "type": "String", "parameters": [32, ]},
                {'name': "unit", "type": "String", "parameters": [32, ]},
                {'name': "description", "type": "String", "parameters": [254, ]},
                {'name': "enabled", "type": "Boolean"},
        ),
        'type': "AttrValue",
        'description': "Size of a storage or of a network connection.",
    },
    'ActionActivityAssignment': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "action_uuid", "type": "ForeignKey", "parameters": ['Action.uuid', ]},
                {'name': "activity_uuid", "type": "ForeignKey", "parameters": ['Activity.uuid', ]},
        ),
        'type': "AttrValue",
        'description': "Mapping between Action and Activity.",
    },
    'ActionSecurityAssignment': {
        'attributes': (
                {'name': "uuid", "type": "Integer", "parameters": [32, ]},
                {'name': "action_uuid", "type": "ForeignKey", "parameters": ['Action.uuid', ]},
                {'name': "security_uuid", "type": "ForeignKey", "parameters": ['Security.uuid', ]},
        ),
        'type': "AttrValue",
        'description': "Mapping between Action and Security.",
    },
}

ACTIONS = (
    {'url': '/tokens', 'action': 'authenticate', 'object': 'tokens', 'method': 'POST'},
    {'url': '/tokens/revoked', 'action': 'revocation_list', 'object': 'tokens', 'method': 'GET'},
    {'url': '/tokens/{token_id}', 'action': 'validate_token', 'object': 'token', 'method': 'GET'},
    {'url': '/tokens/{token_id}', 'action': 'validate_token_head', 'object': 'token', 'method': 'HEAD'},
    {'url': '/tokens/{token_id}', 'action': 'delete_token', 'object': 'token', 'method': 'DELETE'},
    {'url': '/tokens/{token_id}/endpoints', 'action': 'endpoints', 'object': 'endpoints', 'method': 'GET'},
    {'url': '/certificates/ca', 'action': 'ca_cert', 'object': '', 'method': 'GET'},
    {'url': '/certificates/signing', 'action': 'signing_cert', 'object': 'certificates', 'method': 'GET'},
    {'url': '/extensions', 'action': 'get_extensions_info', 'object': 'certificates', 'method': 'GET'},
    {'url': '/extensions/{extension_alias}', 'action': 'get_extension_info', 'object': 'extension', 'method': 'GET'},
    {'url': '/auth/tokens', 'action': 'authenticate_for_token', 'object': 'token', 'method': 'POST'},
    {'url': '/auth/tokens', 'action': 'check_token', 'object': 'token', 'method': 'HEAD'},
    {'url': '/auth/tokens', 'action': 'revoke_token', 'object': 'token', 'method': 'DELETE'},
    {'url': '/auth/tokens', 'action': 'validate_token', 'object': 'token', 'method': 'GET'},
    {'url': '/auth/tokens/OS-PKI/revoked', 'action': 'revocation_list', 'object': 'revocation_list', 'method': 'GET'},
    {'url': '/tenants', 'action': 'get_projects_for_token', 'object': 'tenants', 'method': 'GET'},
    {'url': '/tenants', 'action': 'get_all_projects', 'object': 'tenants', 'method': 'GET'},
    {'url': '/tenants/{tenant_id}', 'action': 'get_project', 'object': 'tenant', 'method': 'GET'},
    {'url': '/tenants/{tenant_id}/users/{user_id}/roles', 'action': 'get_user_roles', 'object': 'roles', 'method': 'GET'},
    {'url': '/users/{user_id}/roles', 'action': 'get_user_roles', 'object': 'roles', 'method': 'GET'},
    {'url': '/users/{user_id}/projects', 'action': 'list_user_projects', 'object': 'tenants', 'method': 'GET'},
    {'url': '/projects/{project_id}/users/{user_id}/roles/{role_id}', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
    {'url': '/projects/{project_id}/groups/{group_id}/roles/{role_id}', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
    {'url': '/projects/{project_id}/users/{user_id}/roles/{role_id}', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
    {'url': '/projects/{project_id}/groups/{group_id}/roles/{role_id}', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
    {'url': '/projects/{project_id}/users/{user_id}/roles', 'action': 'list_grants', 'object': 'roles', 'method': 'GET'},
    {'url': '/projects/{project_id}/groups/{group_id}/roles', 'action': 'list_grants', 'object': 'roles', 'method': 'GET'},
    {'url': '/projects/{project_id}/users/{user_id}/roles/{role_id}', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
    {'url': '/projects/{project_id}/groups/{group_id}/roles/{role_id}', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
    {'url': '/domains/{domain_id}/users/{user_id}/roles/{role_id}', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
    {'url': '/domains/{domain_id}/groups/{group_id}/roles/{role_id}', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
    {'url': '/domains/{domain_id}/users/{user_id}/roles/{role_id}', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
    {'url': '/domains/{domain_id}/groups/{group_id}/roles/{role_id}', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
    {'url': '/domains/{domain_id}/users/{user_id}/roles', 'action': 'list_grants', 'object': 'roles', 'method': 'GET'},
    {'url': '/domains/{domain_id}/groups/{group_id}/roles', 'action': 'list_grants', 'object': 'roles', 'method': 'GET'},
    {'url': '/domains/{domain_id}/users/{user_id}/roles/{role_id}', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
    {'url': '/domains/{domain_id}/groups/{group_id}/roles/{role_id}', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
    {'url': '/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
    {'url': '/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
    {'url': '/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
    {'url': '/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
    {'url': '/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/inherited_to_projects', 'action': 'list_grants', 'object': 'role', 'method': 'GET'},
    {'url': '/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/inherited_to_projects', 'action': 'list_grants', 'object': 'role', 'method': 'GET'},
    {'url': '/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
    {'url': '/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
    {'url': '/users/{user_id}/password', 'action': 'change_password', 'object': 'password', 'method': 'POST'},
    {'url': '/users', 'action': 'list', 'object': 'users', 'method': 'GET'},
    {'url': '/groups/{group_id}/users', 'action': 'list_users_in_group', 'object': 'users', 'method': 'GET'},
    {'url': '/groups/{group_id}/users/{user_id}', 'action': 'add_user_to_group', 'object': 'user', 'method': 'PUT'},
    {'url': '/groups/{group_id}/users/{user_id}', 'action': 'check_user_in_group', 'object': 'user', 'method': 'HEAD'},
    {'url': '/groups/{group_id}/users/{user_id}', 'action': 'remove_user_from_group', 'object': 'user', 'method': 'DELETE'},
    {'url': '/users/{user_id}/groups', 'action': 'list_groups_for_user', 'object': 'groups', 'method': 'GET'},
    {'url': '/users/{user_id}', 'action': "get_user", 'object': 'user', 'method': "GET"},
    {'url': '/OS-KSADM/roles', 'action': 'os-ksadm', 'object': 'roles', 'method': 'GET'},
)
