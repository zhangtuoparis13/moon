/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.intraExtension', ['ngTable', 'ngAnimate', 'mgcrea.ngStrap'])

	.config(function($stateProvider) {
		 
		$stateProvider
	        
		.state('moon.intraExtension', {
			url: '/intraExtension',
			controller: 'IntraExtensionController',
			templateUrl: 'static/moon/app/intra-extension/intra-extension.tpl.html'
		});
		 
	})
	 
	.controller('IntraExtensionController', ['$q', '$scope', '$filter', '$modal', '$translate', 'ngTableParams', 'alertService', 'intraExtensionService', 
	  	                                   		function ($q, $scope, $filter, $modal, $translate, ngTableParams, alertService, intraExtensionService) {

		$scope.form = {};
		
		$scope.intraExtensionsLoading = true;
		$scope.intraExtensions = [];
		
		// key => intraExtension | value: { loading: true/false, tenant: ... }
		$scope.tenantsAssociatedToIntraExtensions = {};
						
		/*
		 * list
		 */
		
		var getData = function() {
			 return $scope.intraExtensions;
		};  	
   	
		$scope.intraExtensionsTable = new ngTableParams({
	    
			page: 1,            // show first page
			count: 10,          // count per page
			sorting: {
				name: 'asc' // initial sorting
			}
   	
		}, {
	    	
			total: function () { return getData().length; }, // length of data
			getData: function($defer, params) {
	        	
				var orderedData = params.sorting() ?
						
					$filter('orderBy')(getData(), params.orderBy()) : getData();
					$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
	        	
			},
			$scope: { $data: {} }
	        
		});
		
		$scope.reloadTable = function() {
			
			$scope.intraExtensionsTable.total($scope.intraExtensions.length);
			$scope.intraExtensionsTable.reload();
			
		};
				   				
		intraExtensionService.intraExtension.query({}).$promise.then(function(data) {
			
			var promises = [];
			
			_.each(data.intra_extensions, function(id) {
				
				promises.push($q(function(resolve) {
												
					intraExtensionService.intraExtension.get({ie_uuid: id}).$promise.then(function(data) {
						resolve(data.intra_extensions);
					});
											
				}));
				
			}); 
											    
		    $q.all(promises).then(function(intraExtensions) {
		    	
		    	$scope.intraExtensions = intraExtensions;
		    			    	
		    	$scope.intraExtensionsLoading = false;
		    	$scope.reloadTable();
		    	
		    });
			
		});
		
		/*
		 * add
		 */
		
		
		
		/*
		 * delete
		 */
		
		
		
		/*
		 * view
		 */
		
		
		 
	}])
	
	.factory('intraExtensionService', function($resource) { 
		
		return {
			
			intraExtension: $resource('./json/intra-extensions/:ie_uuid', {}, {
     	   		query: { method: 'GET', isArray: false },
     	   		get: { method: 'GET', isArray: false }
    	   	}),
    	   	
    	   	tenant: $resource('./json/intra-extensions/:ie_uuid/tenant', {}, {
     	   		query: { method: 'GET', isArray: false }
    	   	}),
     	   	
			policy: $resource('./json/intra-extensions/policies', {}, {
     	   		query: { method: 'GET', isArray: false }
    	   	})
    	   	
		};
		
	})
	 
;