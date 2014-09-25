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
        "subjects": ["user1", "user2"],
        "added_subject": "userx",
        "new_subjects": ["user1", "user2", "userx"],
        "objects": ["vm1", "vm2", "vm3"],
        "added_object": "vmx",
        "new_objects": ["vm1", "vm2", "vm3", "vmx"],
        "subject_category_assignments": {
            "subject_security_level": {
                "user1": ["high"],
                "user2": ["medium"]
            }
        },
        "added_subject_category_assignment1": {"subject_security_levelXXX": {"user2": "high"}},
        "added_subject_category_assignment2": {"subject_security_level": {"user2xxx": "high"}},
        "added_subject_category_assignment3": {"subject_security_level": {"user2": "highxxx"}},
        "added_subject_category_assignment4": {"subject_security_level": {"user2": "medium"}},
        "added_subject_category_assignment5": {"subject_security_level": {"user2": "low"}},
        "new_subject_category_assignments": {
            "subject_security_level": {
                "user1": ["high"],
                "user2": ["medium", "low"]
            }
        },
        "object_category_assignments": {
            "object_security_level": {
                "vm1": ["high"],
                "vm2": ["medium"],
                "vm3": ["low"]
            },
            "action": {
                "vm1": [],
                "vm2": [],
                "vm3": []
            }
        },
        "added_object_category_assignment1": {"object_security_levelxxx": {"vm3": "high"}, "actionxxx": {"vm3": "execute"}},
        "added_object_category_assignment2": {"object_security_level": {"vm3xxx": "high"}, "action": {"vm3xxx": "execute"}},
        "added_object_category_assignment3": {"object_security_level": {"vm3": "highxxx"}, "action": {"vm3": "executexxx"}},
        "added_object_category_assignment4": {"object_security_level": {"vm3": "low"}, "action": {"vm3": ""}},
        "added_object_category_assignment5": {"object_security_level": {"vm3": "high"}, "action": {"vm3": ""}},
        "new_object_category_assignments": {
            "object_security_level": {
                "vm1": ["high"],
                "vm2": ["medium"],
                "vm3": ["low", "high"]
            },
            "action": {
                "vm1": [],
                "vm2": [],
                "vm3": []
            }
        },
        "added_rule": {
            "relation_super": {
                "subject_security_level": "rsrsrsrs",
                "object_security_level": "rorororo",
                "action": "rorororo2"
            }
        },
        "added_rule2": {
            "relation_super": {
                "subject_security_level": "high",
                "object_security_level": "rorororo",
                "action": "rorororo2"
            }
        },
        "added_rule3": {
            "relation_super": {
                "subject_security_level": "low",
                "object_security_level": "low",
                "action": "write"
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
                ["low", "low", "write"]
            ]
        },
        "collaboration": {
            "requesting": {
                "genre": "trust",
                "subject_list": ["user1", "user2"]
            },
            "requested": {
                "genre": "trust",
                "object_list": ["vm1", "vm2"]
            }
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
        "subjects": ["user1", "user2"],
        "added_subject": "userx",
        "new_subjects": ["user1", "user2", "userx"],
        "objects": ["subjects", "objects", "subject_categories", "object_categories", "subject_category_values",
                    "object_category_values", "rules", "subject_category_assignments", "object_category_assignments"],
        "added_object": "objxxx",
        "new_objects": ["subjects", "objects", "subject_categories", "object_categories", "subject_category_values",
                        "object_category_values", "rules", "subject_category_assignments", "object_category_assignments", "objxxx"],
        "subject_category_assignments": {
            "role": {
                "user1": ["admin"],
                "user2": ["dev"]
            }
        },
        "added_subject_category_assignment1": {"roleXXX": {"user2": "admin"}},
        "added_subject_category_assignment2": {"role": {"user2xxx": "admin"}},
        "added_subject_category_assignment3": {"role": {"user2": "adminxxx"}},
        "added_subject_category_assignment4": {"role": {"user2": "dev"}},
        "added_subject_category_assignment5": {"role": {"user2": "admin"}},
        "new_subject_category_assignments": {
            "role": {
                "user1": ["admin"],
                "user2": ["dev", "admin"]
            }
        },
        "object_category_assignments": {
            "action": {
                "subjects": [],
                "objects": [],
                "subject_categories": [],
                "object_categories": [],
                "subject_category_values": [],
                "object_category_values": [],
                "rules": [],
                "subject_category_assignments": [],
                "object_category_assignments": []
            },
            "object_id": {
                "subjects": ["subjects"],
                "objects": ["objects"],
                "subject_categories": ["subject_categories"],
                "object_categories": ["object_categories"],
                "subject_category_values": ["subject_category_values"],
                "object_category_values": ["object_category_values"],
                "rules": ["rules"],
                "subject_category_assignments": ["subject_category_assignments"],
                "object_category_assignments": ["object_category_assignments"]
            }
        },
        "added_object_category_assignment1": {"object_idxxx": {"objects": "objects"}, "actionxxx": {"objects": "execute"}},
        "added_object_category_assignment2": {"object_id": {"objectsxxx": "objects"}, "action": {"objectsxxx": "execute"}},
        "added_object_category_assignment3": {"object_id": {"objects": "objectsxxx"}, "action": {"objects": "executexxx"}},
        "added_object_category_assignment4": {"object_id": {"objects": "objects"}, "action": {"objects": "execute"}},
        "added_object_category_assignment5": {"object_id": {"objects": "subject_categories"}, "action": {"objects": "execute"}},
        "new_object_category_assignments": {
            "action": {
                "subjects": [],
                "objects": [],
                "subject_categories": [],
                "object_categories": [],
                "subject_category_values": [],
                "object_category_values": [],
                "rules": [],
                "subject_category_assignments": [],
                "object_category_assignments": []
            },
            "object_id": {
                "subjects": ["subjects"],
                "objects": ["objects", "subject_categories"],
                "subject_categories": ["subject_categories"],
                "object_categories": ["object_categories"],
                "subject_category_values": ["subject_category_values"],
                "object_category_values": ["object_category_values"],
                "rules": ["rules"],
                "subject_category_assignments": ["subject_category_assignments"],
                "object_category_assignments": ["object_category_assignments"]
            }
        },
        "added_rule": {
            "permission": {
                "role": "rsrsrsrs",
                "object_id": "rorororo",
                "action": "rorororo2"
            }
        },
        "added_rule2": {
            "permission": {
                "role": "admin",
                "object_id": "rorororo",
                "action": "rorororo2"
            }
        },
        "added_rule3": {
            "permission": {
                "role": "dev",
                "object_id": "object_category_assignments",
                "action": "write"
            }
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
        },
        "new_rules": {
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
                ["dev", "object_category_assignments", "read"],
                ["dev", "object_category_assignments", "write"]
            ]
        },
        "collaboration": {
            "requesting": {
                "genre": "trust",
                "subject_list": ["user1", "user2"]
            },
            "requested": {
                "genre": "trust",
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