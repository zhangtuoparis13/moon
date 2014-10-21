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
		
		$scope.add = { intraExtension: null, modal: null, selectedPolicy: null, policies: null };
		
		$scope.add.modal = $modal({scope: $scope, template: 'static/moon/app/intra-extension/intra-extension-add.tpl.html', show: false});
		
		$scope.add.display = function () {
            
			$scope.add.intraExtension = {};
			
			intraExtensionService.policy.query({}, function(data) {
				
				// FIXME service may return an array and not a resource
				$scope.add.policies = data.policies;
				
			});
			
        	$scope.add.modal.$promise.then($scope.add.modal.show);
            
        };
                
        $scope.add.create = function(intraExtension) {
        	
        	if($scope.form.add.$invalid) {
        	
	        	if($scope.form.add.name.$pristine && $scope.form.add.name.$invalid) {
	    			
	        		$scope.form.add.name.$dirty = true;
	        		$scope.form.add.name.$setValidity('required', false);
	    			
	    		} 

				// FIXME when service will return some valid data
	        	
	        	/* if($scope.form.add.policy.$pristine && $scope.form.add.policy.$invalid) {
	    			
	        		$scope.form.add.policy.$dirty = true;
	        		$scope.form.add.policy.$setValidity('required', false);
	    			
	    		} */
        	
        	} else {
        	
        		var policyName = ($scope.add.selectedPolicy) ? $scope.add.selectedPolicy.name : '';
        		        		
        		intraExtensionService.intraExtension.create({}, { name: intraExtension.name, policymodel: policyName }, function(data) {
        			
        			$scope.intraExtensions.push(data);
	        		
	        		$scope.reloadTable();
        			
        			$translate('moon.intraExtension.add.success', { intraExtensionName: intraExtension.name }).then(function (translatedValue) {
	        			alertService.alertSuccess(translatedValue);
	                });	
        			
        		}, function(response) {
        			
        			$translate('moon.intraExtension.add.error', { intraExtensionName: intraExtension.name }).then(function (translatedValue) {
	        			alertService.alertError(translatedValue);
	                });	
        			
        		});
	        	
	        	$scope.add.modal.hide();
        	
    		}
        	
        };
		
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
     	   		get: { method: 'GET', isArray: false },
     	   		create: { method: 'POST' }
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