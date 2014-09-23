results = {
    'authz': {
        'name': 'MLS_metadata',
        'genre': 'authz',
        'subject_categories': ["subject_security_level"],
        'new_subject_category': 'ssss',
        'added_subject_category_list': ["subject_security_level", "ssss"],
        'object_categories': ["object_security_level", "action"],
        'new_object_category': 'oooo',
        'added_object_category_list': ["object_security_level", "action", "oooo"],
        "subject_category_values": {"subject_security_level": ["high", "medium", "low"]},
        "added_subject_category_values": {"subject_security_level": "svsvsvsv"},
        "new_subject_category_values": {"subject_security_level": ["high", "medium", "low", "svsvsvsv"]},
        "object_category_values": {
            "object_security_level": ["high", "medium", "low"],
            "action": ["read", "write", "execute"]
        },
        "added_object_category_values": {"object_security_level": "ovovovov", "action": "ovovovov2"},
        "new_object_category_values": {
            "object_security_level": ["high", "medium", "low", "ovovovov"],
            "action": ["read", "write", "execute", "ovovovov2"]
        },
        "added_rule": {
            "relation_super": {
                "subject_security_level": "rsrsrsrs",
                "object_security_level": "rorororo",
                "action": "rorororo2"
            }
        },
        "rules": {
            "relation_super": [
                ["high", "medium", "read"],
                ["high", "low", "read"],
                ["medium", "low", "read"]
            ]
        },
        "new_rules": {
            "relation_super": [
                ["high", "medium", "read"],
                ["high", "low", "read"],
                ["medium", "low", "read"],
                ["rsrsrsrs", "rorororo", "rorororo2"]
            ]
        }
    },
    'admin': {
        'name': 'RBAC_metadata',
        'genre': 'admin',
        "subject_categories": ["role"],
        'new_subject_category': 'ssss',
        'added_subject_category_list': ["role", "ssss"],
        "object_categories": ["object_id", "action"],
        'new_object_category': 'oooo',
        'added_object_category_list': ["object_id", "action", "oooo"],
        "subject_category_values": {"role": ["admin", "dev"]},
        "added_subject_category_values": {"role": "svsvsvsv"},
        "new_subject_category_values": {"role": ["admin", "dev", "svsvsvsv"]},
        "object_category_values": {
            "action": ["read", "write", "execute"],
            "object_id": ["subjects", "objects", "subject_category_values", "subject_categories",
                          "object_category_values", "object_categories", "rules",
                          "subject_category_assignments","object_category_assignments"]
        },
        "added_object_category_values": {"action": "ovovovov2", "object_id": "ovovovov"},
        "new_object_category_values": {
            "action": ["read", "write", "execute", "ovovovov2"],
            "object_id": ["subjects", "objects", "subject_category_values", "subject_categories",
                          "object_category_values", "object_categories", "rules",
                          "subject_category_assignments","object_category_assignments", "ovovovov"]
        },
        "rules": {
            "permission": [
                ["admin", "subjects", "read"],
                ["admin", "objects", "read"],
                ["admin", "subject_categories", "read"],
                ["admin", "object_categories", "read"],
                ["admin", "subject_category_values", "read"],
                ["admin", "object_category_values", "read"],
                ["admin", "rules", "read"],
                ["admin", "subject_category_assignments", "read"],
                ["admin", "object_category_assignments", "read"],
                ["admin", "subjects", "write"],
                ["admin", "objects", "write"],
                ["admin", "subject_categories", "write"],
                ["admin", "object_categories", "write"],
                ["admin", "subject_category_values", "write"],
                ["admin", "object_category_values", "write"],
                ["admin", "rules", "write"],
                ["admin", "subject_category_assignments", "write"],
                ["admin", "object_category_assignments", "write"],
                ["dev", "subjects", "read"],
                ["dev", "objects", "read"],
                ["dev", "subject_categories", "read"],
                ["dev", "object_categories", "read"],
                ["dev", "subject_category_values", "read"],
                ["dev", "object_category_values", "read"],
                ["dev", "rules", "read"],
                ["dev", "subject_category_assignments", "read"],
                ["dev", "object_category_assignments", "read"]
            ]
        }
    }
}

requests = {
    'authz': [
        {
            'subject': 'user1',
            'object': 'vm1',
            'action': 'read',
            '_result': 'KO',
            '_description': 'permission KO'
        },
        {
            'subject': 'user1',
            'object': 'vm1',
            'action': 'write',
            '_result': 'KO',
            '_description': 'permission KO'
        },
        {
            'subject': 'user1',
            'object': 'vm2',
            'action': 'read',
            '_result': 'OK',
            '_description': 'permission OK'
        },
        {
            'subject': 'user1',
            'object': 'vm2',
            'action': 'write',
            '_result': 'KO',
            '_description': 'permission OK'
        },
        {
            'subject': 'userxxx',
            'object': 'vm2',
            'action': 'read',
            '_result': 'Out of Scope',
            '_description': 'subject out of scope'
        },
        {
            'subject': 'user1',
            'object': 'vmxxx',
            'action': 'read',
            '_result': 'Out of Scope',
            '_description': 'object out of scope'
        }
    ],
    'admin': [
        {
            'subject': 'user1',
            'object': 'subjects',
            'action': 'read',
            '_result': 'OK',
            '_description': 'permission OK'
        },
        {
            'subject': 'user1',
            'object': 'subjects',
            'action': 'write',
            '_result': 'OK',
            '_description': 'permission OK'
        },
        {
            'subject': 'user2',
            'object': 'subjects',
            'action': 'read',
            '_result': 'OK',
            '_description': 'permission OK'
        },
        {
            'subject': 'user2',
            'object': 'subjects',
            'action': 'write',
            '_result': 'KO',
            '_description': 'permission KO'
        },
        {
            'subject': 'userxxx',
            'object': 'subjects',
            'action': 'read',
            '_result': 'Out of Scope',
            '_description': 'subject out of scope'
        },
        {
            'subject': 'user1',
            'object': 'subjectsxxx',
            'action': 'write',
            '_result': 'Out of Scope',
            '_description': 'object out of scope'
        }
    ]
}