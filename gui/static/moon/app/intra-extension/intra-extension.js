/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.intraExtension', ['ngTable', 'ngAnimate', 'mgcrea.ngStrap'])

	.config(function($stateProvider) {
		 
		$stateProvider
		
		.state('moon.intraExtension', {
            abstract: true,
            template: '<div ui-view></div>'
        })
	        
		.state('moon.intraExtension.list', {
			url: '/intraExtension',
			controller: 'IntraExtensionController',
			templateUrl: 'static/moon/app/intra-extension/intra-extension.tpl.html'
		})
		
		.state('moon.intraExtension.configure', {
			url: '/intraExtension/:uuid/configure',
			controller: 'IntraExtensionConfigureController',
			templateUrl: 'static/moon/app/intra-extension/intra-extension-configure.tpl.html',
			resolve: {
				intraExtension: function($stateParams, intraExtensionService) {
					return intraExtensionService.intraExtension.get({ie_uuid: $stateParams.uuid}).$promise;
				}				
			}
		})
		
		.state('moon.intraExtension.rule', {
			url: '/intraExtension/:uuid/rule',
			controller: 'IntraExtensionRuleController',
			templateUrl: 'static/moon/app/intra-extension/intra-extension-rule.tpl.html',
			resolve: {
				intraExtension: function($stateParams, intraExtensionService) {
					return intraExtensionService.intraExtension.get({ie_uuid: $stateParams.uuid}).$promise;
				}				
			}
				
		});
		 
	})
	 
	.controller('IntraExtensionController', ['$q', '$scope', '$state', '$filter', '$modal', '$translate', 'ngTableParams', 'alertService', 'intraExtensionService', 
	  	                                   		function ($q, $scope, $state, $filter, $modal, $translate, ngTableParams, alertService, intraExtensionService) {

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
				_id: 'asc' // initial sorting
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
			$scope.add.policies = [];
			$scope.add.selectedPolicy = null;
			
			intraExtensionService.policy.query({}, function(data) {
				
				// data policies are represented as a map				
				$scope.add.policies = _.keys(data.policies);
				
			});
			
        	$scope.add.modal.$promise.then($scope.add.modal.show);
            
        };
                
        $scope.add.create = function(intraExtension) {
        	
        	if($scope.form.add.$invalid || $scope.add.selectedPolicy == null) {
        	
	        	if($scope.form.add.name.$pristine && $scope.form.add.name.$invalid) {
	    			
	        		$scope.form.add.name.$dirty = true;
	        		$scope.form.add.name.$setValidity('required', false);
	    			
	    		} 
	        	
	        	if($scope.form.add.policy.$pristine && ($scope.form.add.policy.$invalid || $scope.add.selectedPolicy == null)) {
	    			
	        		$scope.form.add.policy.$dirty = true;
	        		$scope.form.add.policy.$setValidity('required', false);
	    			
	    		}
        	
        	} else {
        	        		        		
        		intraExtensionService.intraExtension.create({}, { name: intraExtension.name, policymodel: $scope.add.selectedPolicy }, function(data) {
        			        			        			
        			var created = _(data.intra_extensions).find(function(anIntraExtension) {
	        			return intraExtension.name === anIntraExtension.authz.metadata.name;
	        		});
        			
        			$scope.intraExtensions.push(created);
	        		
	        		$scope.reloadTable();
        			
        			$translate('moon.intraExtension.add.success', { intraExtensionName: intraExtension.name }).then(function (translatedValue) {
	        			alertService.alertSuccess(translatedValue);
	                });	
        			
        			$state.go('moon.intraExtension.configure', { uuid: created._id });
        			
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
		
        $scope.remove = { intraExtension: null, modal: null };
		
		$scope.remove.modal = $modal({scope: $scope, template: 'static/moon/app/intra-extension/intra-extension-delete.tpl.html', show: false});
		
		$scope.remove.display = function (intraExtension) {
            
			$scope.remove.intraExtension = intraExtension;
        	$scope.remove.modal.$promise.then($scope.remove.modal.show);
            
        };
                
        $scope.remove.remove = function(intraExtension) {
        	        	
        	intraExtensionService.intraExtension.remove({ie_uuid: intraExtension._id}, function(data) {
        		
        		$scope.intraExtensions = _.chain($scope.intraExtensions).reject({_id: intraExtension._id}).value();
        		
        		$scope.reloadTable();
        		
        		$translate('moon.intraExtension.remove.success', { intraExtensionName: intraExtension.authz.metadata.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
        		
        	}, function(response) {
        		
        		$translate('moon.intraExtension.remove.error', { intraExtensionName: intraExtension.authz.metadata.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
        		
        	});
        	
        	$scope.remove.modal.hide();
        	
        };
				
		 
	}])
	
	.controller('IntraExtensionConfigureController', ['$q', '$scope', '$state', '$stateParams', '$filter', '$modal', '$translate', 'intraExtension', 'ngTableParams', 'alertService', 'intraExtensionService', 
	  	                                   		function ($q, $scope, $state, $stateParams, $filter, $modal, $translate, intraExtension, ngTableParams, alertService, intraExtensionService) {
		
		$scope.intraExtension = intraExtension.intra_extensions;
		
		$scope.subject = { subjects: [], categories: [], selected: null };
		$scope.object = { objects: [], categories: [], selected: null };
		 
		intraExtensionService.subject.query({ie_uuid: $scope.intraExtension._id }, function(data) {
			$scope.subject.subjects = data.subjects;
		});
		
		intraExtensionService.object.query({ie_uuid: $scope.intraExtension._id }, function(data) {
			$scope.object.objects = data.objects;
		});
		
	}])
	
	.controller('IntraExtensionRuleController', ['$q', '$scope', '$state', '$stateParams', '$filter', '$modal', '$translate', 'intraExtension', 'ngTableParams', 'alertService', 'intraExtensionService', 
	  	                                   		function ($q, $scope, $state, $stateParams, $filter, $modal, $translate, intraExtension, ngTableParams, alertService, intraExtensionService) {
		
		$scope.intraExtension = intraExtension.intra_extensions;
		
	}])
	
	.factory('intraExtensionService', function($resource) { 
		
		return {
			
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
    	   	
    	   	subject: $resource('./json/intra-extensions/:ie_uuid/subjects', {}, {
    	   		query: { method: 'GET', isArray: false },
     	   		get: { method: 'GET', isArray: false }
    	   	}),
    	   	
    	   	object: $resource('./json/intra-extensions/:ie_uuid/objects', {}, {
    	   		query: { method: 'GET', isArray: false },
     	   		get: { method: 'GET', isArray: false }
    	   	})
    	   	
		};
		
	})
	 
;