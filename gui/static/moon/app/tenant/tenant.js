/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.tenant', ['ngTable', 'ngAnimate', 'mgcrea.ngStrap'])

	.config(function($stateProvider) {
		 
		$stateProvider
	        
		.state('moon.tenant', {
			url: '/tenant',
			controller: 'TenantController',
            templateUrl: 'static/moon/app/tenant/tenant.tpl.html'
		});
		 
	})
	 
	.controller('TenantController', ['$scope', '$filter', '$modal', '$translate', 'ngTableParams', 'alertService', 'tenantService', 
	                                   function ($scope, $filter, $modal, $translate, ngTableParams, alertService, tenantService) {

		$scope.tenantsLoading = true;
		$scope.tenants = [];
		 
		/*
		 * list
		 */
		 
		var getData = function() {
			 return $scope.tenants;
		};  	
    	
		$scope.tenantsTable = new ngTableParams({
	    
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
    	
		tenantService.project.query({}, function(data) {
        	
			$scope.tenantsLoading = false;
			$scope.tenants = data.projects;
			        	
			$scope.tenantsTable.total($scope.tenants.length);
			$scope.tenantsTable.reload();
        	
		}, function(response) {
			
			$scope.tenantsLoading = false;
			$scope.tenants = [];
			
			$translate('moon.tenant.error.query').then(function (translatedValue) {
    			alertService.alertError(translatedValue);
            });	
			
		});
		 
		/*
		 * search
		 */
		 
		$scope.query = '';
	    	
		$scope.search = function (tenant){
		    
			if (tenant.name.indexOf($scope.query)!=-1 
					|| tenant.domain.indexOf($scope.query)!=-1) {
				
		        return true;
		    
			}
		    
			return false;
		        
		};
		
		$scope.reset = function() {
			$scope.query = '';
		};
		
		/*
		 * view
		 */
		
		$scope.view = { tenant: null, modal: null, subjects: [], objects: [], roles: [], groups: [], roleAssignments: [], groupAssignments: [] };
		
		$scope.view.modal = $modal({scope: $scope, template: 'static/moon/app/tenant/tenantView.tpl.html', show: false});
		
		$scope.view.display = function (tenant) {
            
        	$scope.view.tenant = tenant;
        	$scope.view.modal.$promise.then($scope.view.modal.show);
            
        };
                		 
	}])
	 
	.factory('tenantService', function($resource) { 
                                   	
		return {
                 	   	
			project: $resource('./pip/projects/:project_uuid', {}, {
     	   		query: { method: 'GET', isArray: false },
     	   		get: { method: 'GET', isArray: false }
    	   	}),
    	   	
    	   	subject: $resource('./pip/projects/:project_uuid/users/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: false },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	object: $resource('./pip/projects/:project_uuid/objects/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	role: $resource('./pip/projects/:project_uuid/roles/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	group: $resource('./pip/projects/:project_uuid/groups/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	roleAssigment: $resource('./pip/projects/:project_uuid/assigments/roles/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	groupAssigment: $resource('./pip/projects/:project_uuid/assigments/groups/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	})
        
        };
    
    })
	 	 
;