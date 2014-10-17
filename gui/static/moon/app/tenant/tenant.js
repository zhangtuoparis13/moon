/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.tenant', ['ngTable', 'ngAnimate', 'mgcrea.ngStrap', 'NgSwitchery'])

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

		$scope.form = {};
		
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
		
		$scope.reloadTable = function() {
			
			$scope.tenantsTable.total($scope.tenants.length);
			$scope.tenantsTable.reload();
			
		};
    	
		tenantService.tenant.query({}, function(data) {
        	
			$scope.tenantsLoading = false;
			$scope.tenants = data.projects;
			
			$scope.reloadTable();
			        	        	
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
		 * add
		 */
		
		$scope.defaultTenant = function() { 
			return { name: null, description: null, enabled: true, domain: 'Default'} 
		}; 
		
		$scope.add = { tenant: null, modal: null };
		
		$scope.add.modal = $modal({scope: $scope, template: 'static/moon/app/tenant/tenantAdd.tpl.html', show: false});
		
		$scope.add.display = function () {
            
			$scope.add.tenant = $scope.defaultTenant();
        	$scope.add.modal.$promise.then($scope.add.modal.show);
            
        };
                
        $scope.add.create = function(tenant) {
        	
        	if($scope.form.add.$invalid) {
        	
	        	if($scope.form.add.name.$pristine && $scope.form.add.name.$invalid) {
	    			
	        		$scope.form.add.name.$dirty = true;
	        		$scope.form.add.name.$setValidity('required', false);
	    			
	    		} 
	        	
	        	if($scope.form.add.domain.$pristine && $scope.form.add.domain.$invalid) {
	    			
	        		$scope.form.add.domain.$dirty = true;
	        		$scope.form.add.domain.$setValidity('required', false);
	    			
	    		}
        	
        	} else {
        	
	        	tenantService.tenant.create({}, tenant, function(data) {
	        		
	        		var created = _(data.projects).find(function(aTenant) {
	        			return tenant.name === aTenant.name;
	        		});
	        		
	        		$scope.tenants.push(created);
	        		
	        		$scope.reloadTable();
	        		
	        		$translate('moon.tenant.add.success', { tenantName: tenant.name }).then(function (translatedValue) {
	        			alertService.alertSuccess(translatedValue);
	                });	
	        		
	        	}, function(response) {
	        		
	        		$translate('moon.tenant.add.error', { tenantName: tenant.name }).then(function (translatedValue) {
	        			alertService.alertError(translatedValue);
	                });	
	        		
	        	});
	        	
	        	$scope.add.modal.hide();
        	
    		}
        	
        };
		
		/*
		 * delete
		 */
		
        $scope.remove = { tenant: null, modal: null };
		
		$scope.remove.modal = $modal({scope: $scope, template: 'static/moon/app/tenant/tenantDelete.tpl.html', show: false});
		
		$scope.remove.display = function (tenant) {
            
			$scope.remove.tenant = tenant;
        	$scope.remove.modal.$promise.then($scope.remove.modal.show);
            
        };
                
        $scope.remove.remove = function(tenant) {
        	        	
        	tenantService.tenant.remove({project_uuid: tenant.uuid}, function(data) {
        		
        		$scope.tenants = _.chain($scope.tenants).reject({uuid: tenant.uuid}).value();
        		
        		$scope.reloadTable();
        		
        		$translate('moon.tenant.remove.success', { tenantName: tenant.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
        		
        	}, function(response) {
        		
        		$translate('moon.tenant.remove.error', { tenantName: tenant.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
        		
        	});
        	
        	$scope.remove.modal.hide();
        	
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