/**
 * 
 * @TODO intra_extensions.name is an Array; change it to a String
 * @FIXME intra_extensions.tenant_uuid is never filled
 * 
 * @author arnaud marhin<arnaud.marhin@orange.com>
 * 
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
			templateUrl: 'static/moon/app/intra-extension/intra-extension.tpl.html',
			resolve: {
				superExtensions: function(tenantService) {
            		return tenantService.rest.superExtention.query({}).$promise;
            	}				
			}
		})
		
		.state('moon.intraExtension.configure', {
			url: '/intraExtension/:uuid/configure',
			controller: 'IntraExtensionConfigureController',
			templateUrl: 'static/moon/app/intra-extension/intra-extension-configure.tpl.html',
			resolve: {
				intraExtension: function($stateParams, intraExtensionService) {
					return intraExtensionService.rest.intraExtension.get({ie_uuid: $stateParams.uuid}).$promise;
				}
			}
		})
		
		.state('moon.intraExtension.rule', {
			url: '/intraExtension/:uuid/rule',
			controller: 'IntraExtensionRuleController',
			templateUrl: 'static/moon/app/intra-extension/intra-extension-rule.tpl.html',
			resolve: {
				intraExtension: function($stateParams, intraExtensionService) {
					return intraExtensionService.rest.intraExtension.get({ie_uuid: $stateParams.uuid}).$promise;
				}
			}
				
		});
		 
	})
	 
	.controller('IntraExtensionController', ['$q', '$scope', '$state', '$filter', '$modal', '$translate', 'ngTableParams', 'alertService', 'intraExtensionService', 'tenantService', 'superExtensions',
	  	                                   		function ($q, $scope, $state, $filter, $modal, $translate, ngTableParams, alertService, intraExtensionService, tenantService, superExtensions) {

		$scope.form = {};
		
		$scope.intraExtensionsLoading = true;
		$scope.intraExtensions = [];
								
		/*
		 * ---- list
		 */
		
		var getData = function() {
			 return $scope.intraExtensions ? $scope.intraExtensions : [];
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
	        	
				var orderedData = params.sorting() ? $filter('orderBy')(getData(), params.orderBy()) : getData();
					
				$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
	        	
			},
			$scope: { $data: {} }
	        
		});
		
		$scope.reloadTable = function() {
			
			$scope.intraExtensionsTable.total($scope.intraExtensions.length);
			$scope.intraExtensionsTable.reload();
			
		};
		
		intraExtensionService.findAll(function(data) {
			
			$scope.intraExtensions = data;
			
			_($scope.intraExtensions).each(function(anIntraExtension) {
				
				anIntraExtension.tenant_uuid = null;
				anIntraExtension.tenant = null;
				
				var extension = _(superExtensions.super_extensions).find(function(anExtension) {
					return _.first(anExtension.intra_extension_uuids) === anIntraExtension._id;
				});
				
				if(extension) {
					
					anIntraExtension.tenant_uuid = extension.tenant_uuid;
					
					tenantService.findOne(anIntraExtension.tenant_uuid).then(function(tenant) {
						anIntraExtension.tenant = _.first(tenant.projects);
					});
					
				}
				
			});
			
			$scope.intraExtensionsLoading = false;
	    	$scope.reloadTable();
			
		});
		
		/*
		 * ---- search
		 */
		 
		$scope.search = { query: '', find: null, reset: null };
			    	
		$scope.search.find = function (intraExtension){
		    
			if (_.first(intraExtension.name).indexOf($scope.search.query)!=-1 
					|| intraExtension.authz.metadata.model.indexOf($scope.search.query)!=-1) {
				
		        return true;
		    
			}
		    
			return false;
		        
		};
		
		$scope.search.reset = function() {
			$scope.search.query = '';
		};
		
		/*
		 * ---- add
		 */
		
		$scope.add = { intraExtension: null, modal: null, selectedPolicy: null, policies: null };
		
		$scope.add.modal = $modal({scope: $scope, template: 'static/moon/app/intra-extension/intra-extension-add.tpl.html', show: false});
		
		$scope.add.display = function () {
            
			$scope.add.intraExtension = {};
			$scope.add.policies = [];
			$scope.add.selectedPolicy = null;
			
			intraExtensionService.rest.policy.query({}, function(data) {
				
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
        	        		        		
        		intraExtensionService.rest.intraExtension.create({}, { name: intraExtension.name, policymodel: $scope.add.selectedPolicy }, function(data) {
        			        			        			        			
        			$scope.intraExtensions.push(data.intra_extensions);
	        		
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
		 * ---- delete
		 */
		
        $scope.remove = { intraExtension: null, modal: null };
		
		$scope.remove.modal = $modal({scope: $scope, template: 'static/moon/app/intra-extension/intra-extension-delete.tpl.html', show: false});
		
		$scope.remove.display = function (intraExtension) {
            
			$scope.remove.intraExtension = intraExtension;
        	$scope.remove.modal.$promise.then($scope.remove.modal.show);
            
        };
                
        $scope.remove.remove = function(intraExtension) {
        	        	
        	intraExtensionService.rest.intraExtension.remove({ie_uuid: intraExtension._id}, function(data) {
        		
        		$scope.intraExtensions = _.chain($scope.intraExtensions).reject({_id: intraExtension._id}).value();
        		
        		$scope.reloadTable();
        		
        		$translate('moon.intraExtension.remove.success', { intraExtensionName: _.first(intraExtension.name) }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
        		
        	}, function(response) {
        		
        		$translate('moon.intraExtension.remove.error', { intraExtensionName: _.first(intraExtension.name) }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
        		
        	});
        	
        	$scope.remove.modal.hide();
        	
        };
				
		 
	}])
	
	.controller('IntraExtensionConfigureController', ['$q', '$scope', '$state', '$stateParams', '$filter', '$modal', '$translate', 'ngTableParams', 'alertService', 'tenantService', 'intraExtensionService', 'intraExtension', 
	  	                                   		function ($q, $scope, $state, $stateParams, $filter, $modal, $translate, ngTableParams, alertService, tenantService, intraExtensionService, intraExtension) {
		
		$scope.form = {};
		
		$scope.intraExtension = intraExtension.intra_extensions;
				
		/*
		 * ---- subject
		 */
		
		$scope.subject = { subjects: [], 
						   categories: [], 
						   selected: [], 
						   add: {}, 
						   remove: {} };
		
		intraExtensionService.rest.subject.query({ie_uuid: $scope.intraExtension._id }, function(data) {
						
			var promises = [];
			
			_(data.subjects).each(function(subjectId) {
				promises.push(tenantService.rest.subject.get({ project_uuid: $scope.intraExtension.tenant_uuid, user_uuid: subjectId }));
			});
			
			$q.all(promises).then(function(data) {
				$scope.subject.subjects = data;
			});
			
		});
		
		/*
		 * -- add
		 */
		
		$scope.getDefaultSubject = function() {
			
			return { name: '', 
					 domain: 'Default', 
					 enabled: false, 
					 project: '', 
					 password: '', 
					 description: '' };
					 
		};
		
		$scope.subject.add = { intraExtension: null, 
							   subject: $scope.getDefaultSubject(), 
							   modal: $modal({ scope: $scope, 
								   			   template: 'static/moon/app/intra-extension/intra-extension-configure-subject-add.tpl.html', 
								   			   show: false }) };
				
		$scope.subject.add.display = function (intraExtension) {
			
			$scope.subject.add.intraExtension = intraExtension;
			$scope.subject.add.subject = $scope.getDefaultSubject();
			
			$scope.subject.add.modal.$promise.then($scope.subject.add.modal.show);
            
        };
        
        $scope.subject.add.create = function(intraExtension, subject) {
        	
        	if($scope.form.add.subject.$invalid) {
            	
	        	if($scope.form.add.subject.name.$pristine && $scope.form.add.subject.name.$invalid) {
	    			
	        		$scope.form.add.subject.name.$dirty = true;
	        		$scope.form.add.subject.name.$setValidity('required', false);
	    			
	    		} 
	        	
	        	if($scope.form.add.subject.domain.$pristine && $scope.form.add.subject.domain.$invalid) {
	    			
	        		$scope.form.add.subject.domain.$dirty = true;
	        		$scope.form.add.subject.domain.$setValidity('required', false);
	    			
	    		}
	        	
	        	if($scope.form.add.subject.project.$pristine && $scope.form.add.subject.project.$invalid) {
	    			
	        		$scope.form.add.subject.project.$dirty = true;
	        		$scope.form.add.subject.project.$setValidity('required', false);
	    			
	    		}

				if($scope.form.add.subject.password.$pristine && $scope.form.add.subject.password.$invalid) {
					
					$scope.form.add.subject.password.$dirty = true;
					$scope.form.add.subject.password.$setValidity('required', false);
					
				}
        	
        	} else {
        		
        		intraExtensionService.rest.subject.create({ie_uuid: intraExtension._id}, subject, function(data) {
        			
        			$scope.subject.subjects.push(subject);
        			$scope.subject.selected.push(subject);
        			
        			$translate('moon.intraExtension.configure.subject.add.success', { subjectName: subject.name }).then(function (translatedValue) {
	        			alertService.alertSuccess(translatedValue);
	                });	
        			
        		}, function(error) {
        			
        			$translate('moon.intraExtension.configure.subject.add.error', { subjectName: subject.name }).then(function (translatedValue) {
	        			alertService.alertError(translatedValue);
	                });	
        			
        		});
        		
        		$scope.subject.add.modal.hide();
        		
        	}
        	
        };
        
        /*
         * -- delete
         */
        
        /*
         * ---- object
         */
        
        $scope.object = { objects: [], categories: [], selected: null };
		 
		intraExtensionService.rest.object.query({ie_uuid: $scope.intraExtension._id }, function(data) {
			$scope.object.objects = data.objects;
		});
		
		
		
	}])
	
	.controller('IntraExtensionRuleController', ['$q', '$scope', '$state', '$stateParams', '$filter', '$modal', '$translate', 'intraExtension', 'ngTableParams', 'alertService', 'intraExtensionService', 
	  	                                   		function ($q, $scope, $state, $stateParams, $filter, $modal, $translate, intraExtension, ngTableParams, alertService, intraExtensionService) {
		
		$scope.intraExtension = intraExtension.intra_extensions;
		
	}])
	
	.factory('intraExtensionService', function($q, $resource) { 
		
		
		
	})
	 
;