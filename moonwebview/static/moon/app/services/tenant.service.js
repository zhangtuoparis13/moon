/**
 * Service providing access to the tenants
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';

	angular
		.module('moon')
				.factory('tenantService', tenantService);
	
	tenantService.$inject = ['$q', '$resource' , 'REST_URI' ];
	
	function tenantService($q, $resource, REST_URI) {
	                                   	
		return {
			
			data: {
                 	   	
				tenant: $resource(REST_URI.TENANTS + "/:tenant_uuid", {}, {
	     	   		query: { method: 'GET', isArray: false },
				get: { method: 'GET', isArray: false },
	     	   		create: { method: 'POST' },
	     	   		remove: { method: 'DELETE' }
	    	   	}),

				// /!\ Duplicated API here (see intraextension.service.js)
				// /!\ ":user_uuid": deprecated variable naming, but still used in the by some calls
	    	   	subject: $resource( REST_URI.INTRAEXTENSION + '/:project_uuid/subjects/:user_uuid', {}, {
	    	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false }    	   		
	    	   	}),

				// /!\ Duplicated API here (see intraextension.service.js)
	    	   	object: $resource(REST_URI.INTRAEXTENSION + '/:project_uuid/objects/:object_uuid', {}, {
	    	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false }    	   		
	    	   	}),

				// /!\ Duplicated API here (see intraextension.service.js)
	    	   	role: $resource(REST_URI.INTRAEXTENSION + '/:project_uuid/roles', {}, {
	    	   		query: { method: 'GET', isArray: false }	
	    	   	}),
	    	   	
	    	   	subjectRole: $resource(REST_URI.INTRAEXTENSION + '/:project_uuid/users/:user_uuid/roles', {}, {
	    	   		query: { method: 'GET', isArray: false }	
	    	   	}),
	    	   	
	    	   	group: $resource(REST_URI.INTRAEXTENSION + '/:project_uuid/groups', {}, {
	    	   		query: { method: 'GET', isArray: false }		
	    	   	}),
	    	   	
	    	   	subjectGroup: $resource(REST_URI.INTRAEXTENSION + '/:project_uuid/users/:user_uuid/groups', {}, {
	    	   		query: { method: 'GET', isArray: false }		
	    	   	}),
	    	   	
	    	   	roleAssigment: $resource(REST_URI.INTRAEXTENSION + '/:project_uuid/assignments/roles/:user_uuid', {}, {
	    	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false }    	   		
	    	   	}),
	    	   	
	    	   	groupAssigment: $resource(REST_URI.INTRAEXTENSION + '/:project_uuid/assignments/groups/:user_uuid', {}, {
	    	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false }    	   		
	    	   	}),
	    	   	
	    	   	map: $resource(REST_URI.SUPEREXTENTION +'/tenants/:tenant_uuid/intra_extensions/:intra_extension_uuid', {}, {
	    	   		create: { method: 'POST' },
	    	   		remove: { method: 'DELETE' }
	    	   	}),
	    	   	
			/*
			 * Not yet implemented
			 */
	    	   	superExtention: $resource(REST_URI.SUPEREXTENTION, {}, {
	    	   		query: { method: 'GET' }
	    	   	})
    	   	
			},
			
			findOne: function(uuid) {
	   			return this.data.tenant.get({tenant_uuid: uuid}).$promise; //project_uu
	   		},

			findMany: function() {
				return this.data.tenant.query({tenant_uuid: ''}).$promise.then(function(listTenants) {
				var result = [];
				var i;
				for (i in listTenants) {
					if (listTenants[i].id)
						result.push(listTenants[i]);
				}
				return result;
				});
							}
        
        };
    
    }
	
})();
