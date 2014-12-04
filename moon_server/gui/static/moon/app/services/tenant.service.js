/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';

	angular
		.module('moon')
				.factory('tenantService', tenantService);
	
	tenantService.$inject = ['$q', '$resource'];
	
	function tenantService($q, $resource) { 
	                                   	
		return {
			
			data: {
                 	   	
				tenant: $resource('./pip/projects/:project_uuid', {}, {
	     	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false },
	     	   		create: { method: 'POST' },
	     	   		remove: { method: 'DELETE' }
	    	   	}),
	    	   	
	    	   	subject: $resource('./pip/projects/:project_uuid/users/:user_uuid', {}, {
	    	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false }    	   		
	    	   	}),
	    	   	
	    	   	object: $resource('./pip/projects/:project_uuid/objects/:object_uuid', {}, {
	    	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false }    	   		
	    	   	}),
	    	   	
	    	   	role: $resource('./pip/projects/:project_uuid/roles', {}, {
	    	   		query: { method: 'GET', isArray: false }	
	    	   	}),
	    	   	
	    	   	subjectRole: $resource('./pip/projects/:project_uuid/users/:user_uuid/roles', {}, {
	    	   		query: { method: 'GET', isArray: false }	
	    	   	}),
	    	   	
	    	   	group: $resource('./pip/projects/:project_uuid/groups', {}, {
	    	   		query: { method: 'GET', isArray: false }		
	    	   	}),
	    	   	
	    	   	subjectGroup: $resource('./pip/projects/:project_uuid/users/:user_uuid/groups', {}, {
	    	   		query: { method: 'GET', isArray: false }		
	    	   	}),
	    	   	
	    	   	roleAssigment: $resource('./pip/projects/:project_uuid/assignments/roles/:user_uuid', {}, {
	    	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false }    	   		
	    	   	}),
	    	   	
	    	   	groupAssigment: $resource('./pip/projects/:project_uuid/assignments/groups/:user_uuid', {}, {
	    	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false }    	   		
	    	   	}),
	    	   	
	    	   	map: $resource('./json/super-extensions/tenants/:tenant_uuid/intra_extensions/:intra_extension_uuid', {}, {
	    	   		create: { method: 'POST' },
	    	   		remove: { method: 'DELETE' }
	    	   	}),
	    	   	
	    	   	superExtention: $resource('./json/super-extensions', {}, {
	    	   		query: { method: 'GET' }
	    	   	})
    	   	
			},
			
			findOne: function(uuid) {
	   			return this.data.tenant.get({project_uuid: uuid}).$promise;
	   		}
        
        };
    
    };
	
})();
