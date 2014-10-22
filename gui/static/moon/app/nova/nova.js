/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.nova', ['ngResource'])

	.factory('novaService', function($resource) { 
                                   	
        return {
            
            image: $resource('./pip/nova/images', {}, {
            	query: {method: 'GET', isArray: false}
     	   	}),
     	   	
     	   	flavor: $resource('./pip/nova/flavors', {}, {
            	query: {method: 'GET', isArray: false}
     	   	})
        
        };
    
    })
    
;