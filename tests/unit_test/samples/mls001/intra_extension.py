results = {
    'trust': {
        "collaboration": {
            "requesting": {
                "vent_uuid": "xxooxxoo",
                "genre": "trust",
                "subject_list": ["user1", "user2"]
            },
            "requested": {
                "vent_uuid": "xxooxxoo",
                "genre": "trust",
                "object_list": ["vm1", "vm2"]
            }
        }
    },
    "coordinate": {
        "collaboration": {
            "requesting": {
                "vent_uuid": "xxooxxoo",
                "genre": "coordinate",
                "subject_list": ["user1", "user2"]
            },
            "requested": {
                "vent_uuid": "xxooxxoo",
                "genre": "coordinate",
                "object_list": ["object_category_assignments"]
            }
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