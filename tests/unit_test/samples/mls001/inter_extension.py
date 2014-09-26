results = {
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

