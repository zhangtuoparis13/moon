/**
# Copyright 2015 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
 */

(function() {

	'use strict';

	angular
	
		.module('moon', ['ngResource',
		                 'ngRoute',                                            
	                     'ui.router',
	                     'ui.bootstrap',
	                     'ngTable',
	                     'ngCookies',
	                     'pascalprecht.translate',
	                     'ngAnimate',
	                     'mgcrea.ngStrap',
	                     'NgSwitchery',
	                     'ui.select',
	                     'toaster'])
	
	                     .config(configurer)
	                     .run(runner);
	
	/*
	 * configurer
	 */
	
	configurer.$inject = ['$urlRouterProvider', '$translateProvider', '$stateProvider', 'uiSelectConfig'];
	
	function configurer($urlRouterProvider, $translateProvider, $stateProvider, uiSelectConfig) {
		
	    /*
	     * translate
	     */
	    
	    $translateProvider
	        .useStaticFilesLoader({
	            prefix: 'static/moon/i18n/',
	            suffix: '.json'
		    })
		    .preferredLanguage('en')
		    .useCookieStorage();
	    
	    /*
	     * ui-select
	     */
	    
	    uiSelectConfig.theme = 'selectize';
	    
	    /*
	     * routes
	     */
	    
	    $urlRouterProvider.when('', '/tenant');
	    $urlRouterProvider.otherwise('/404');
	    
	    configureDefaultRoutes($stateProvider);	    
	    
	    configureTenantRoutes($stateProvider);
	    
	    configureIntraExtensionRoutes($stateProvider);
	    
	    configureInterExtensionRoutes($stateProvider);
	   		
	};
	
	function configureDefaultRoutes($stateProvider) {
		
		$stateProvider
	    
		    .state('moon', {
		        abstract: true,
		        template: '<div ui-view></div>'
		    })
		    
		    .state('moon.404', {
	    		url: '/404',
	            templateUrl: 'static/moon/app/common/404.tpl.html'
	        });
		
		return $stateProvider;
		
	};
	
	function configureTenantRoutes($stateProvider) {
		
		 $stateProvider
	        
	        .state('moon.tenant', {
				abstract: true,
		        template: '<div ui-view></div>'
	        })
	        		
			.state('moon.tenant.list', {
				url: '/tenant',
				templateUrl: 'static/moon/app/tenant/tenant-list.tpl.html',
				controller: 'TenantListController',
				controllerAs: 'list',
	            resolve: {
	            	/*superExtensions: function(tenantService) {
	            		return tenantService.data.superExtention.query().$promise;
	            	},*/
	            	tenants: function(tenantService) {
	            		return tenantService.data.tenant.query().$promise;
	            	}
	            }
			});
		 
		 return $stateProvider;
		
	};
	
	function configureIntraExtensionRoutes($stateProvider) {
		
		$stateProvider
		
			.state('moon.intraExtension', {
				abstract: true,
		        template: '<div ui-view></div>'
	        })
			
			.state('moon.intraExtension.list', {
				url: '/intraExtension',
	            templateUrl: 'static/moon/app/intra-extension/intra-extension-list.tpl.html',
	            controller: 'IntraExtensionListController',
	            controllerAs: 'list',
	            resolve: {
	            	intraExtensions: function(intraExtensionService) {
	            		return intraExtensionService.findAll();
	            	}
	            }
	        })			
	        
	        .state('moon.intraExtension.edit', {
		        abstract: true,
		        url: '/intraExtension/:uuid',
		        template: '<div ui-view></div>',
		        resolve: {
					intraExtension: function($stateParams, intraExtensionService) {
						return intraExtensionService.data.intraExtension.get({ie_uuid: $stateParams.uuid}).$promise;
					},
					tenant: function(tenantService, intraExtension) {
						return tenantService.findMany();//findOne(intraExtension.intra_extensions.tenant_uuid);
					},
					subjects: function(intraExtensionService, intraExtension) {
						//@todo: UPDT query
						//window.alert(_.first(intraExtension.intra_extensions).id);
						return intraExtensionService.data.subject.subject.query({ie_uuid: _.first(intraExtension.intra_extensions).id, subject_uuid: 0 }).$promise;
					},
					subjectCategories: function(intraExtensionService, intraExtension) {
						//@todo: UPDT query
						return intraExtensionService.data.subject.category.query({ie_uuid: _.first(intraExtension.intra_extensions).id, category_name: 0}).$promise;
					},
					subjectCategoryValues: function(intraExtensionService, intraExtension) {
						//@todo: UPDT query
						return intraExtensionService.data.subject.categoryValue.query({ie_uuid: _.first(intraExtension.intra_extensions).id,  category: 0, value: 0}).$promise;
					},
					subjectAssignments: function(intraExtensionService, intraExtension) {
						//@todo: UPDT query
						return intraExtensionService.data.subject.assignment.query({ie_uuid: _.first(intraExtension.intra_extensions).id, subject_id: 0, category_id: 0, value: 0 }).$promise;
					},
					objects: function(intraExtensionService, intraExtension) {
						//@todo: UPDT query
						return intraExtensionService.data.object.object.query({ie_uuid: _.first(intraExtension.intra_extensions).id, object_uuid: 0 }).$promise;
					},
					objectCategories: function(intraExtensionService, intraExtension) {
						//@todo: UPDT query
						return intraExtensionService.data.object.category.query({ie_uuid: _.first(intraExtension.intra_extensions).id, category_name:0 }).$promise;
					},
					objectCategoryValues: function(intraExtensionService, intraExtension) {
						//@todo: UPDT query
						return intraExtensionService.data.object.categoryValue.query({ie_uuid: _.first(intraExtension.intra_extensions).id, category: 0, value: 0 }).$promise;
					},
					objectAssignments: function(intraExtensionService, intraExtension) {
						//@todo: UPDT query
						return intraExtensionService.data.object.assignment.query({ie_uuid: _.first(intraExtension.intra_extensions).id, category_id: 0, value: 0}).$promise;
					}
				}
		    })
	        
	        .state('moon.intraExtension.edit.configuration', {
				url: '/configure',
				templateUrl: 'static/moon/app/intra-extension/intra-extension-configure.tpl.html',
				controller: 'IntraExtensionConfigurationController',
				controllerAs: 'conf'
			})
			
			.state('moon.intraExtension.edit.rule', {
				url: '/rule',
				templateUrl: 'static/moon/app/intra-extension/intra-extension-rule.tpl.html',
				controller: 'IntraExtensionRuleController',
				controllerAs: 'list',
				resolve: {
					rules: function($stateParams, intraExtensionService) {
						// /!\ @todo: Watch out ! $stateParams.uuid can't be resolved !
						return intraExtensionService.data.rule.query({ie_uuid: $stateParams.uuid}).$promise;
					},
					hasMLSPolicy: function(intraExtensionService, intraExtension) {
						return intraExtensionService.hasMLSPolicy(intraExtension);
					},
					hasRBACPolicy: function(intraExtensionService, intraExtension) {
						return intraExtensionService.hasRBACPolicy(intraExtension);
					}
				}
			});
		
		return $stateProvider;
		
	};
	
	function configureInterExtensionRoutes($stateProvider) {
		
		$stateProvider
		
			.state('moon.interExtension', {
				abstract: true,
		        template: '<div ui-view></div>'
	        })
			
			.state('moon.interExtension.list', {
	            url: '/interExtension',
	            templateUrl: 'static/moon/app/inter-extension/inter-extension-list.tpl.html',
	            controller: 'InterExtensionListController',
	            controllerAs: 'list'
	        });
		
		return $stateProvider;
		
	};
	
	/*
	 * runner
	 */
	
	runner.$inject = ['$rootScope', '$state', '$modal', '$translate', 'alertService'];
	
	function runner($rootScope, $state, $modal, $translate, alertService) {
		
		$rootScope.transitionModal = $modal({ scope: $rootScope, template: 'static/moon/app/common/waiting.tpl.html', backdrop: 'static', show: false });
						
		$rootScope.$on('$stateChangeStart', stateChangeStart),
		$rootScope.$on('$stateChangeSuccess', stateChangeSuccess),
		$rootScope.$on('$stateChangeError', stateChangeError)
	    
	    function stateChangeStart() {
	        $rootScope.transitionModal.$promise.then($rootScope.transitionModal.show);
	    };
	    
	    function stateChangeSuccess() {
			$rootScope.transitionModal.hide();
	    };
	    
	    function stateChangeError(event, toState, toParams, fromState, fromParams, error) {
	    	
	    	var stacktrace = getStacktrace(event, toState, toParams, fromState, fromParams, error);
	    
	    	$translate('moon.global.error', { stacktrace: stacktrace }).then(function (translatedValue) {
    			alertService.alertError(translatedValue);
            });
	    	
			$rootScope.transitionModal.hide();
						
	    };
	    
	    function getStacktrace(event, toState, toParams, fromState, fromParams, error) {
	    	
	    	var stacktrace = {};
	    	
	    	stacktrace.status = error.status;
	    	stacktrace.message = error.statusText;
	    	stacktrace.state = toState;
	    	stacktrace.params = toParams;
	    	
	    	return stacktrace;
	    	
	    };
		
	};
	
})();
