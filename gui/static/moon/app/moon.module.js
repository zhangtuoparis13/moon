/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
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
	                     'ui.select'])
	
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
	    
	    /*
	     * states
	     */
	    
	    $stateProvider
	    
		    .state('moon', {
		        abstract: true,
		        template: '<div ui-view></div>'
		    })
		    
		    .state('moon.404', {
	    		url: '/404',
	            templateUrl: 'static/moon/app/common/404.tpl.html'
	        })
	        		
			.state('moon.tenant', {
				url: '/tenant',
				templateUrl: 'static/moon/app/tenant/tenant-list.tpl.html',
				controller: 'TenantListController',
				controllerAs: 'list',
	            resolve: {
	            	superExtensions: function(tenantService) {
	            		return tenantService.data.superExtention.query().$promise;
	            	},
	            	tenants: function(tenantService) {
	            		return tenantService.data.tenant.query().$promise;
	            	}
	            }
			})
			
			.state('moon.intraExtension', {
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
	        
	        .state('moon.intraExtensionConfiguration', {
				url: '/intraExtension/:uuid/configure',
				templateUrl: 'static/moon/app/intra-extension/intra-extension-configure.tpl.html',
				controller: 'IntraExtensionConfigurationController',
				controllerAs: 'conf',
				resolve: {
					intraExtension: function($stateParams, intraExtensionService) {
						return intraExtensionService.data.intraExtension.get({ie_uuid: $stateParams.uuid}).$promise;
					},
					tenant: function(tenantService, intraExtension) {
						return tenantService.findOne(intraExtension.intra_extensions.tenant_uuid);
					},
					subjects: function(intraExtensionService, intraExtension) {
						return intraExtensionService.data.subject.query({ie_uuid: intraExtension.intra_extensions._id }).$promise;
					},
					objects: function(intraExtensionService, intraExtension) {
						return intraExtensionService.data.object.query({ie_uuid: intraExtension.intra_extensions._id }).$promise;
					}
				}
			})
			
			.state('moon.interExtension', {
	            url: '/interExtension',
	            templateUrl: 'static/moon/app/inter-extension/inter-extension-list.tpl.html',
	            controller: 'InterExtensionListController',
	            controllerAs: 'list'
	        });
		
	};
	
	/*
	 * runner
	 */
	
	runner.$inject = ['$rootScope', '$state', '$modal'];
	
	function runner($rootScope, $state, $modal) {
		
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
	    
	    function stateChangeError() {
			$rootScope.transitionModal.hide();
	    };
		
	};
	
})();
