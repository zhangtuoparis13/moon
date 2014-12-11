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