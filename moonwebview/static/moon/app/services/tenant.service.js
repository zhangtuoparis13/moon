/**
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
                 	   	
				tenant: $resource(REST_URI.TENANTS, {}, {
	     	   		query: { method: 'GET', isArray: true },
					get: { method: 'GET', isArray: true },
	     	   		create: { method: 'POST' }
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
	    	   	
	    	   	superExtention: $resource(REST_URI.SUPEREXTENTION, {}, {
	    	   		query: { method: 'GET' }
	    	   	})
    	   	
			},
			
			findOne: function(uuid) {
				//window.alert("" +uuid + JSON.stringify(this.data.tenant.get({project_uuid: uuid})));
	   			return this.data.tenant.get({id: uuid}).$promise; //project_uu
	   		}
        
        };
    
    }
	
})();
