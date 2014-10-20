/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

'use strict';

var moonApp = angular.module('moonApp', ['ngRoute',                                            
                                         'ui.router',
                                         'ui.bootstrap',
                                         'ngTable',
                                         'ngCookies',
                                         'pascalprecht.translate',
                                         'ngAnimate',
                                         'mgcrea.ngStrap',
                                         'ui.select',
                                         'moonApp.common',
                                         'moonApp.tenant',
                                         'moonApp.intraExtension',
                                         'moonApp.interExtension'])

    .config(['$urlRouterProvider', '$translateProvider', '$stateProvider', 'uiSelectConfig',
        function($urlRouterProvider, $translateProvider, $stateProvider, uiSelectConfig) {
    	
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

        }
    
    ])

    .run(['$rootScope', '$state', '$modal',
        function($rootScope, $state, $modal) {
    	
        	$rootScope.transitionModal = $modal({scope: $rootScope, template: 'static/moon/app/common/waiting.tpl.html', backdrop: 'static', show: false});
    	
            $rootScope.$on('$stateChangeStart', function (toState, toParams, fromState, fromParams) {
                $rootScope.transitionModal.$promise.then($rootScope.transitionModal.show);
            });

            $rootScope.$on('$stateChangeSuccess', function(){
        		$rootScope.transitionModal.hide();
            });

            $rootScope.$on('$stateChangeError',  function(){
        		$rootScope.transitionModal.hide();
            });
                        
        }
    
    ]);

;
