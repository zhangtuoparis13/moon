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
    "intra_extensions": {
        "authz": [
            {
                'subject': 'user1',
                'object': 'vm1',
                'action': 'read',
                '_result': 'KO'
            },
            {
                'subject': 'user1',
                'object': 'vm2',
                'action': 'read',
                '_result': 'OK'
            }
        ],
        "admin": [
            {
                'subject': 'user2',
                'object': 'subjects',
                'action': 'read',
                '_result': 'OK'
            },
            {
                'subject': 'user2',
                'object': 'subjects',
                'action': 'write',
                '_result': 'KO'
            }
        ]
    },
    "inter_extensions": {
        'trust': {
            "subject_list": ["user1", "user2"],
            "object_list": ["vm1", "vm2"],
            "action": "read",
            "requests": [
                {"subject": "userX", "object": "vm2", "action": "read", "result": "KO"},
                {"subject": "user1", "object": "vmX", "action": "read", "result": "KO"},
                {"subject": "user1", "object": "vm2", "action": "write", "result": "KO"},
                {"subject": "user1", "object": "vm2", "action": "read", "result": "OK"}
            ]
        },
        "coordinate": {
            "subject_list": ["user1", "user2"],
            "object_list": ["object_category_assignments"],
            "action": "read",
            "requests": [
                {"subject": "userX", "object": "object_category_assignments", "action": "read", "result": "KO"},
                {"subject": "user1", "object": "object_category_assignmentsX", "action": "read", "result": "KO"},
                {"subject": "user1", "object": "object_category_assignments", "action": "write", "result": "KO"},
                {"subject": "user1", "object": "object_category_assignments", "action": "read", "result": "OK"}
            ]
        }
    }
}
