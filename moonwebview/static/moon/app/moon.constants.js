/**
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
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.constant('DEFAULT_CST', {
				DOMAIN: {
					DEFAULT: 'Default'
				}
			})
			.constant('INTRA_EXTENSION_CST', { 
				POLICY: {
					RBAC: {
						NAME: 'RBAC',
						META_RULE: 'permission'
					},
					MLS: {
						NAME: 'MLS',
						META_RULE: 'relation_super'
					}
				},
				OBJECT: {
					SERVERS: {
						category: "object",
						description: "",
						enabled: true,
						name: "servers",
						tenant: null,
						uuid: "servers"
					}
				},
				RULE: {
					ID_PREFIX: 'rule_'
				}
			})
		.constant('TENANTS_REST_URI','test/tenant_db.json')
		.constant('USERS_REST_URI','test/user_db.json')
		.constant('INTRAEXTENSION_REST_URI','test/intraextension_db.json')
		.constant('EXTRAEXTENTION_REST_URI','test/extraextension_db.json');

})();
