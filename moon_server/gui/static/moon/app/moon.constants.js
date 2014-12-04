/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
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
			});

})();
