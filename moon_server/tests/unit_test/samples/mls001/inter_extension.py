# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
    },
    "delegate_collaboration_admin": {
        "before": {
            'subject': 'user1',
            'object': 'collaboration',
            'action': 'destroy',
            '_result': 'KO',
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
            "_result": "[InterExtension] Delegate: Add Inter_Extension_User Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "list",
            "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "create",
            "_result": "[InterExtension] Delegate: Add Inter_Extension_Admin Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "create",
            "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "destroy",
            "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "destroy",
            "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
        },
        {
            "delegator_id": "user1",
            "privilege": "delegate",
            "_result": "[InterExtension] Delegate: Add Inter_Extension_Root Privilege"
        },
        {
            "delegator_id": "user1",
            "privilege": "delegate",
            "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
        }
    ]
}

