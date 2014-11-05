/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationAddSubjectCategoryValueController', IntraExtensionConfigurationAddSubjectCategoryValueController);
	
	IntraExtensionConfigurationAddSubjectCategoryValueController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationAddSubjectCategoryValueController($scope, $translate, alertService, intraExtensionService) {
		
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
        		
        		intraExtensionService.data.subject.categoryValue.create({ie_uuid: add.intraExtension._id}, {category_id: add.category.name, value: add.value }, createSuccess, createError);
        		        		        		
        	}	
			
			function createSuccess(data) {
    							
    			$translate('moon.intraExtension.configure.subject.categoryValue.add.success', { valueName: add.value }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionSubjectCategoryValueCreatedSuccess', { category: add.category, value: add.value });
    			
    		};
    		
    		function createError(reason) {
    			
    			$translate('moon.intraExtension.configure.subject.categoryValue.add.error', { valueName: add.value }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionSubjectCategoryValueCreatedError', { category: add.category, value: add.value });
    			        			
    		};
			
		};		
		
	};
	
})();