/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionAddController', IntraExtensionAddController);
	
	IntraExtensionAddController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionAddController($scope, $translate, alertService, intraExtensionService) {
		
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
        	
        	if(add.form.$invalid || add.selectedPolicy == null) {
        	
	        	if(add.form.name.$pristine && add.form.name.$invalid) {
	    			
	        		add.form.name.$dirty = true;
	        		add.form.name.$setValidity('required', false);
	    			
	    		} 
	        	
	        	if(add.form.policy.$pristine && (add.form.policy.$invalid || add.selectedPolicy == null)) {
	    			
	        		add.form.policy.$dirty = true;
	        		add.form.policy.$setValidity('required', false);
	    			
	    		}
        	
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