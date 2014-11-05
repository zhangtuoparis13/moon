/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationAddObjectCategoryValueController', IntraExtensionConfigurationAddObjectCategoryValueController);
	
	IntraExtensionConfigurationAddObjectCategoryValueController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationAddObjectCategoryValueController($scope, $translate, alertService, intraExtensionService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		add.intraExtension = $scope.intraExtension;
		add.category = $scope.category;
		add.value = null;
		
		add.create = addValue;
		
		/*
		 * 
		 */
		
		function addValue() {
			
			if(add.form.$invalid) {
            	
	        	if(add.form.value.$pristine && add.form.value.$invalid) {
	    			
	        		add.form.value.$dirty = true;
	        		add.form.value.$setValidity('required', false);
	    			
	    		}
        	
        	} else {
        		
        		intraExtensionService.data.object.categoryValue.create({ie_uuid: add.intraExtension._id}, {category_id: add.category.name, value: add.value }, createSuccess, createError);
        		        		        		
        	}	
			
			function createSuccess(data) {
    							
    			$translate('moon.intraExtension.configure.object.categoryValue.add.success', { valueName: add.value }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionObjectCategoryValueCreatedSuccess', { category: add.category, value: add.value });
    			
    		};
    		
    		function createError(reason) {
    			
    			$translate('moon.intraExtension.configure.object.categoryValue.add.error', { valueName: add.value }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionObjectCategoryValueCreatedError', { category: add.category, value: add.value });
    			        			
    		};
			
		};		
		
	};
	
})();