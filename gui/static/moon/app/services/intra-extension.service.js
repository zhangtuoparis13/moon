/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';

	angular
		.module('moon')
				.factory('intraExtensionService', intraExtensionService);
	
	intraExtensionService.$inject = ['$q', '$resource'];
	
	function intraExtensionService($q, $resource) {
		
		return {
			
			data: {
			
				intraExtension: $resource('./json/intra-extensions/:ie_uuid', {}, {
	     	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false },
	     	   		create: { method: 'POST' },
	     	   		remove: { method: 'DELETE' }
	    	   	}),
	    	   	    	   	
	    	   	tenant: $resource('./json/intra-extensions/:ie_uuid/tenant', {}, {
	     	   		query: { method: 'GET', isArray: false }
	    	   	}),
	     	   	
				policy: $resource('./json/intra-extensions/policies', {}, {
	     	   		query: { method: 'GET', isArray: false }
	    	   	}),
	    	   	
	    	   	subject: {
	    	   		
	    	   		subject: $resource('./json/intra-extensions/:ie_uuid/subjects/:subject_uuid', {}, {
		    	   		query: { method: 'GET', isArray: false },
		     	   		get: { method: 'GET', isArray: false },
		     	   		create: { method: 'POST' },
		     	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	category: $resource('./json/intra-extensions/:ie_uuid/subject_categories/:category_name', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	categoryValue: $resource('./json/intra-extensions/:ie_uuid/subject_category_values/:category/:value', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	assignment: $resource('./json/intra-extensions/:ie_uuid/subject_assignments', {}, {
		    	   		query: { method: 'GET', isArray: false }
		    	   	})
	    	   		
	    	   	},
	    	   	
	    	   	object: {
	    	   		
	    	   		object: $resource('./json/intra-extensions/:ie_uuid/objects', {}, {
		    	   		query: { method: 'GET', isArray: false },
		     	   		get: { method: 'GET', isArray: false },
		     	   		create: { method: 'POST' },
		     	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	category: $resource('./json/intra-extensions/:ie_uuid/object_categories/:category_name', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	categoryValue: $resource('./json/intra-extensions/:ie_uuid/object_category_values', {}, {
		    	   		query: { method: 'GET', isArray: false }
		    	   	}),		    	   	
		    	   	
		    	   	assignment: $resource('./json/intra-extensions/:ie_uuid/object_assignments', {}, {
		    	   		query: { method: 'GET', isArray: false }
		    	   	})
	    	   		
	    	   	}    	   	
    	   	
			},
			
			findAll: function() {

    	   		var _self = this;
    	   		
    	   		return this.data.intraExtension.query().$promise.then(function(result) {

    	   			return _.map(result.intra_extensions, function(uuid) {
    	   				return _self.findOne(uuid);
    	   			}); 

    	   		}).then(function(uuids) {
	   					    	   			
    	   			return $q.all(uuids).then(function(result) {
    	   				
    	   				return _(result).map(function(resource) {
    	   					return resource.intra_extensions;
    	   				});
    	   				    	   				    	   				
    	   			});

	   			});

	   		},
	   		
	   		findOne: function(uuid) {
	   			
	   			return this.data.intraExtension.get({ie_uuid: uuid}).$promise;
	   			
	   		},
	   		
	   		findSome: function(uuids) {
	   			
	   			var _self = this;
	   			
	   			var promises = _(uuids).map(function(uuid) {
	   				return _self.findOne(uuid);
	   			});
	   			
	   			return $q.all(promises).then(function(result) {
	   				
	   				return _(result).map(function(resource) {
	   					return resource.intra_extensions;
	   				});
	   				
	   			});
	   			
	   		}
    	   	
		};
		
	};
	
})();
