/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.common', ['ngResource', 'ngAnimate', 'mgcrea.ngStrap'])

    .controller('HeaderController', ['$rootScope', '$scope', '$state', '$translate', 
                                     function ($rootScope, $scope, $state, $translate) {       
    		
	    	$rootScope.changeLocale = function(localeKey, event) {
				
	            event.preventDefault();
	            
	            $translate.use(localeKey);
	            $translate.preferredLanguage(localeKey);
	                            
	        };
    	
        }
        
    ])  
    
    .controller('FooterController', ['$scope', '$modal', 'VersionService',
                                     function ($scope, $modal, VersionService) {       
    	
    		$scope.browsersModal = $modal({scope: $scope, template: 'static/moon/app/common/compatibility.tpl.html', show: false});
    		
    		$scope.browsersCompliance = function() {
    			$scope.browsersModal.$promise.then($scope.browsersModal.show);    			
    		};
    		
    		$scope.version = 'SNAPSHOT';
    		$scope.version = VersionService.version.get(function(data) { 
    			$scope.version = data.version;
    		});
    	
        }
        
    ])  
    
    .factory('AlertService', ['$rootScope', '$timeout', 
                              function($rootScope, $timeout) {
    	
            var alertService = null;
        
            $rootScope.alerts = [];
            
            return alertService = {
            
            		add: function(type, msg, timeout) {
            			
	                    $rootScope.alerts.push({
	                        type: type,
	                        msg: msg,
	                        close: function() {
	                            return alertService.closeAlert(this);
	                        }
	                    });
	
	                    if (timeout) {
	                        $timeout(function(){
	                            alertService.closeAlert(this);
	                        }, timeout);
	                    }
	                    
	                },
	                
	                closeAlert: function(alert) {
	                    return this.closeAlertIdx($rootScope.alerts.indexOf(alert));
	                },
	                
	                closeAlertIdx: function(index) {
	                    return $rootScope.alerts.splice(index, 1);
	                },
	                
	                alertError: function alertError(msg){
	                    this.add("danger", msg, 7000);
	                },
	                
	                alertSuccess: function alertSucess(msg){
	                    this.add("success", msg, 7000);
	                },
	                
	                alertInfo: function alertSucess(msg){
	                    this.add("info", msg, 7000);
	                }
	                
            };
            
        }
    
    ])
        
    .factory('BrowserService', ['$rootScope', 
                               
        function($rootScope) {
    	
            return {
                
            	sayswho: function(){
            	 
            		var ua= navigator.userAgent, tem, 
            	    
            		M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
            	    
            		if(/trident/i.test(M[1])){
            	        tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
            	        return 'IE '+(tem[1] || '');
            	    }
            	    
            		if(M[1]=== 'Chrome'){
            	        tem= ua.match(/\bOPR\/(\d+)/);
            	        if(tem!= null) return 'Opera '+tem[1];
            	    }
            	    
            		M= M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
            	    
            		if((tem= ua.match(/version\/(\d+)/i))!= null) M.splice(1, 1, tem[1]);
            	    
            	    return M.join(' ');
            	    
            	}
            
            };
            
        }
    
    ])
    
    .factory('VersionService', function($resource) { 
                                   	
        return {
            
            version:  $resource('static/moon/version.json', {}, {
            	get: {method: 'GET', isArray: false}
     	   	})
        
        };
    
    })
    
;
