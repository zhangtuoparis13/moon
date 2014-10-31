/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.factory('alertService', alertService);
	
	alertService.$inject = ['$rootScope', '$timeout'];
	
	function alertService($rootScope, $timeout) {
				
        $rootScope.alerts = [];
		
		var service = {
				
				addAlert: addAlert,
			
				closeAlert: closeAlert,
				closeAlertIdx: closeAlertIdx,
			
				alertError: alertError,
				alertSuccess: alertSuccess,
				alertInfo: alertInfo				
				
			};
        
        return service;
                
        function closeAlert(alert) {
            return this.closeAlertIdx($rootScope.alerts.indexOf(alert));
        };
        
        function closeAlertIdx(index) {
            return $rootScope.alerts.splice(index, 1);
        };
        
        function addAlert(type, msg, timeout) {
        	
    		var _self = this;
			
	        $rootScope.alerts.push({
	            type: type,
	            msg: msg,
	            close: function() {
	                return _self.closeAlert(this);
	            }
	        });
	
	        if (timeout) {
	            $timeout(function(){
	            	_self.closeAlert(this);
	            }, timeout);
	        }
	        
	    };
        
        function alertError(msg){
        	this.addAlert("danger", msg, 7000);
        };
        
        function alertSuccess(msg){
        	this.addAlert("success", msg, 7000);
        };
        
        function alertInfo(msg){
        	this.addAlert("info", msg, 7000);
        };
		
	};
	
})();
