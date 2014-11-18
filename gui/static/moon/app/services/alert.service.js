/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.factory('alertService', alertService);
	
	alertService.$inject = ['$rootScope', '$timeout', 'toaster'];
	
	function alertService($rootScope, $timeout, toaster) {
						
		var service = {
							
				alertError: alertError,
				alertSuccess: alertSuccess,
				alertInfo: alertInfo				
				
			};
        
        return service;
                        
        function alertError(msg){
        	toaster.pop('error', null, msg, 5000);
        };
        
        function alertSuccess(msg){
        	toaster.pop('success', null, msg, 5000);
        };
        
        function alertInfo(msg){
        	toaster.pop('note', null, msg, 5000);
        };
		
	};
	
})();
