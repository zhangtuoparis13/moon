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
                         'ui.select',
                         'moonApp.tenant',
                         'moonApp.intraExtension',
                         'moonApp.interExtension',
                         'moonApp.nova'])

    .config(configurer)
    .run(runner);
	
	/*
	 * configurer
	 */
	
	configurer.$inject = ['$urlRouterProvider', '$translateProvider', '$stateProvider', 'uiSelectConfig'];
	
	function configurer($urlRouterProvider, $translateProvider, $stateProvider, uiSelectConfig) {
		
		$urlRouterProvider.when('', '/tenant');
		
        $urlRouterProvider.otherwise('/404');

        $stateProvider.state('moon', {
            abstract: true,
            template: '<div ui-view></div>'
        })
        
        $stateProvider.state('moon.404', {
        		url: '/404',
                templateUrl: 'static/moon/app/common/404.tpl.html'
            });

        $translateProvider
            .useStaticFilesLoader({
                prefix: 'static/moon/i18n/',
                suffix: '.json'
        })
        .preferredLanguage('en')
        .useCookieStorage();
        
        uiSelectConfig.theme = 'selectize';
		
	};
	
	/*
	 * runner
	 */
	
	runner.$inject = ['$rootScope', '$state', '$modal'];
	
	function runner($rootScope, $state, $modal) {
		
		$rootScope.transitionModal = $modal({ scope: $rootScope, template: 'static/moon/app/common/waiting.tpl.html', backdrop: 'static', show: false });
    	
        $rootScope.$on('$stateChangeStart', stateChangeStart);
        $rootScope.$on('$stateChangeSuccess', stateChangeSuccess);
        $rootScope.$on('$stateChangeError', stateChangeError);
        
        function stateChangeStart(toState, toParams, fromState, fromParams) {
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
