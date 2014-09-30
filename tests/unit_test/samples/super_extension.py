results = {
    "list_mappings": [
        {
            "tenant_uuid": "admin",
            "intra_extension_uuids": ["super_extension"]
        }
    ],
    "create_mapping": [
        {
            "tenant_uuid": "tenant1",
            "intra_extension_uuid": "intra_extension1",
            "_result": "[SuperExtension] Create Mapping for No Existing Mapping: OK"
        },
        {
            "tenant_uuid": "tenant1",
            "intra_extension_uuid": "intra_extension2",
            "_result": "[SuperExtension] Create Mapping for Existing Tenant: OK"
        },
        {
            "tenant_uuid": "tenant1",
            "intra_extension_uuid": "intra_extension1",
            "_result": "[SuperExtension Error] Create Mapping for Existing Mapping"
        }
    ],
    "destroy_mapping": [
        {
            "tenant_uuid": "tenant1",
            "intra_extension_uuid": "intra_extension1",
            "_result": "[SuperExtension] Destroy Mapping: OK"
        },
        {
            "tenant_uuid": "tenant1",
            "intra_extension_uuid": "intra_extension2",
            "_result": "[SuperExtension] Destroy Mapping: OK"
        },
        {
            "tenant_uuid": "tenant1",
            "intra_extension_uuid": "intra_extension1",
            "_result": "[SuperExtension Error] Destroy Unknown Mapping"
        }
    ],
    "delegate_mapping_admin": {
        "before": {
            'subject': 'user1',
            'object': 'mapping',
            'action': 'destroy',
            '_result': 'Out of Scope',
            '_description': 'user1 no delegated ---------------- Out of Scope'
        },
        "after": {
            'subject': 'user1',
            'object': 'mapping',
            'action': 'destroy',
            '_result': 'OK',
            '_description': 'user1 delegated ---------------- OK'
        }
    },
    "delegate_mapping_privilege": [
        {
            "delegator_id": "user1",
            "privilege": "list",
            "_result": "[SuperExtension] Delegate: Add Super_User Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "list",
            "_result": "[SuperExtension ERROR] Mapping Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "create",
            "_result": "[SuperExtension] Delegate: Add Super_Admin Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "create",
            "_result": "[SuperExtension ERROR] Mapping Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "destroy",
            "_result": "[SuperExtension ERROR] Mapping Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "destroy",
            "_result": "[SuperExtension ERROR] Mapping Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "delegate",
            "_result": "[SuperExtension] Delegate: Add Super_Root Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "delegate",
            "_result": "[SuperExtension ERROR] Mapping Delegate: Privilege Exists"
        }
    ],
    "delegate_collaboration_admin": {
        "before": {
            'subject': 'user1',
            'object': 'collaboration',
            'action': 'destroy',
            '_result': 'Out of Scope',
            '_description': 'user1 no delegated ---------------- Out of Scope'
        },
        "after": {
            'subject': 'user1',
            'object': 'collaboration',
            'action': 'destroy',
            '_result': 'OK',
            '_description': 'user1 delegated ---------------- OK'
        }
    },
    "delegate_collaboration_privilege": [
        {
            "delegator_id": "user1",
            "privilege": "list",
            "_result": "[SuperExtension] Delegate: Add Inter_Extension_User Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "list",
            "_result": "[SuperExtension ERROR] Collaboration Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "create",
            "_result": "[SuperExtension] Delegate: Add Inter_Extension_Admin Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "create",
            "_result": "[SuperExtension ERROR] Collaboration Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "destroy",
            "_result": "[SuperExtension ERROR] Collaboration Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "destroy",
            "_result": "[SuperExtension ERROR] Collaboration Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "delegate",
            "_result": "[SuperExtension] Delegate: Add Inter_Extension_Root Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "delegate",
            "_result": "[SuperExtension ERROR] Collaboration Delegate: Privilege Exists"
        }
    ]
}

requests = [
    {
        'subject': 'admin',
        'object': 'mapping',
        'action': 'list',
        '_result': 'OK',
        '_description': 'permission OK'
    },
    {
        'subject': 'admin',
        'object': 'mapping',
        'action': 'create',
        '_result': 'OK',
        '_description': 'permission OK'
    },
    {
        'subject': 'admin',
        'object': 'mapping',
        'action': 'destroy',
        '_result': 'OK',
        '_description': 'permission OK'
    },
    {
        'subject': 'adminXXX',
        'object': 'mapping',
        'action': 'list',
        '_result': 'Out of Scope',
        '_description': 'permission Out of Scope'
    },
    {
        'subject': 'admin',
        'object': 'mappingXXX',
        'action': 'list',
        '_result': 'Out of Scope',
        '_description': 'permission Out of Scope'
    },
    {
        'subject': 'admin',
        'object': 'mapping',
        'action': 'listXXX',
        '_result': 'KO',
        '_description': 'permission KO'
    }
]

requests2 = [
    {
        'subject': 'admin',
        'object': 'collaboration',
        'action': 'list',
        '_result': 'OK',
        '_description': 'permission OK'
    },
    {
        'subject': 'admin',
        'object': 'collaboration',
        'action': 'create',
        '_result': 'OK',
        '_description': 'permission OK'
    },
    {
        'subject': 'admin',
        'object': 'collaboration',
        'action': 'destroy',
        '_result': 'OK',
        '_description': 'permission OK'
    },
    {
        'subject': 'adminXXX',
        'object': 'collaboration',
        'action': 'list',
        '_result': 'Out of Scope',
        '_description': 'permission Out of Scope'
    },
    {
        'subject': 'admin',
        'object': 'collaborationXXX',
        'action': 'list',
        '_result': 'Out of Scope',
        '_description': 'permission Out of Scope'
    },
    {
        'subject': 'admin',
        'object': 'collaboration',
        'action': 'listXXX',
        '_result': 'KO',
        '_description': 'permission KO'
    }
]