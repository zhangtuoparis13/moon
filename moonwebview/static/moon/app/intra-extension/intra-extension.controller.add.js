/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionAddController', IntraExtensionAddController);
	
	IntraExtensionAddController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'intraExtensionService'];
	
	function IntraExtensionAddController($scope, $translate, alertService, formService, intraExtensionService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		
		add.intraExtension = {};
		add.policies = [];
		add.selectedPolicy = null;
		
		add.create = createIntraExtension;
		
		resolvePolicies();
		
		/*
		 * 
		 */
		
		function resolvePolicies() {
			
			return intraExtensionService.data.policy.query().$promise.then(function(data) {
				
				// data policies are represented as a map				
				add.policies = _.keys(data.policies);
				
				return add.policies;
				
			});
			
		};
                
        function createIntraExtension(intraExtension) {
        	
        	if(formService.isInvalid(add.form)) {
        		
        		formService.checkFieldsValidity(add.form);
        	        	
        	} else {
        	        		        		
        		intraExtensionService.data.intraExtension.create({}, { name: intraExtension.name, policymodel: $scope.add.selectedPolicy }, createSuccess, createError);
        			        	        	
    		}
        	
        	function createSuccess(data) {
    			
    			$translate('moon.intraExtension.add.success', { intraExtensionName: intraExtension.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionCreatedSuccess', data.intra_extensions);	
    			
    		};
    		
    		function createError(reason) {
    			
    			$translate('moon.intraExtension.add.error', { intraExtensionName: intraExtension.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
    			
    			$scope.$emit('event:intraExtensionCreatedError');
    			
    		};
        	
        };
		
	};
	
})();