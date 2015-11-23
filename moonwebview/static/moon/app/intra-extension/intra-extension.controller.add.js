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
		
		/**
		 * This function return an array of all policies/template ids
		 */
		function resolvePolicies() {
			
			return intraExtensionService.data.policy.query().$promise.then(function(data) {
				// data policies are represented as a map				
				add.policies = _.keys(data);
				//Dirty cleaning
				add.policies = _.without(add.policies,"$promise","$resolved");
				return add.policies;
				
			});
			
		};
                
        function createIntraExtension(intraExtension) {
        	
        	if(formService.isInvalid(add.form)) {
        		
        		formService.checkFieldsValidity(add.form);
        	        	
        	} else {
        	        		        		
        		intraExtensionService.data.intraExtension.create({}, { intra_extensions_name: intraExtension.name, intra_extensions_model: $scope.add.selectedPolicy, intra_extensions_description: $scope.add.description}, createSuccess, createError);
        			        	        	
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
