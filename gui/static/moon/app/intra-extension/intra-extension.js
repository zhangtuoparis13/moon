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
		
		
		
	}])
	
	.controller('IntraExtensionRuleController', ['$q', '$scope', '$state', '$stateParams', '$filter', '$modal', '$translate', 'intraExtension', 'ngTableParams', 'alertService', 'intraExtensionService', 
	  	                                   		function ($q, $scope, $state, $stateParams, $filter, $modal, $translate, intraExtension, ngTableParams, alertService, intraExtensionService) {
		
		$scope.intraExtension = intraExtension.intra_extensions;
		
	}])
	
	.factory('intraExtensionService', function($q, $resource) { 
		
		
		
	})
	 
;