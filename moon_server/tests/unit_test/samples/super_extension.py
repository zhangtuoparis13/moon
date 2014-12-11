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
    # "delegate_collaboration_admin": {
    #     "before": {
    #         'subject': 'user1',
    #         'object': 'collaboration',
    #         'action': 'destroy',
    #         '_result': 'Out of Scope',
    #         '_description': 'user1 no delegated ---------------- Out of Scope'
    #     },
    #     "after": {
    #         'subject': 'user1',
    #         'object': 'collaboration',
    #         'action': 'destroy',
    #         '_result': 'OK',
    #         '_description': 'user1 delegated ---------------- OK'
    #     }
    # },
    # "delegate_collaboration_privilege": [
    #     {
    #         "delegator_id": "user1",
    #         "privilege": "list",
    #         "_result": "[InterExtension] Delegate: Add Inter_Extension_User Privilege"
    #     },
    #     {
    #         "delegator_id": "user1",
    #         "privilege": "list",
    #         "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
    #     },
    #     {
    #         "delegator_id": "user1",
    #         "privilege": "create",
    #         "_result": "[InterExtension] Delegate: Add Inter_Extension_Admin Privilege"
    #     },
    #     {
    #         "delegator_id": "user1",
    #         "privilege": "create",
    #         "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
    #     },
    #     {
    #         "delegator_id": "user1",
    #         "privilege": "destroy",
    #         "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
    #     },
    #     {
    #         "delegator_id": "user1",
    #         "privilege": "destroy",
    #         "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
    #     },
    #     {
    #         "delegator_id": "user1",
    #         "privilege": "delegate",
    #         "_result": "[InterExtension] Delegate: Add Inter_Extension_Root Privilege"
    #     },
    #     {
    #         "delegator_id": "user1",
    #         "privilege": "delegate",
    #         "_result": "[InterExtension ERROR] Collaboration Delegate: Privilege Exists"
    #     }
    # ]
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