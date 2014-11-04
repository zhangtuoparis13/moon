/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationAddObjectCategoryController', IntraExtensionConfigurationAddObjectCategoryController);
	
	IntraExtensionConfigurationAddObjectCategoryController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationAddObjectCategoryController($scope, $translate, alertService, intraExtensionService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		add.intraExtension = $scope.intraExtension;
		add.category = { name: '' };
		
		add.create = addCategory;
		
		/*
		 * 
		 */
		
		function addCategory() {
			
			if(add.form.$invalid) {
            	
	        	if(add.form.name.$pristine && add.form.name.$invalid) {
	    			
	        		add.form.name.$dirty = true;
	        		add.form.name.$setValidity('required', false);
	    			
	    		}
        	
        	} else {
        		
        		intraExtensionService.data.object.category.create({ie_uuid: add.intraExtension._id}, {category_id: add.category.name}, createSuccess, createError);
        		        		        		
        	}	
			
			function createSuccess(data) {
    							
    			$translate('moon.intraExtension.configure.object.category.add.success', { categoryName: add.category.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionObjectCategoryCreatedSuccess', add.category);
    			
    		};
    		
    		function createError(reason) {
    			
    			$translate('moon.intraExtension.configure.object.category.add.error', { categoryName: add.category.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionObjectCategoryCreatedError', add.category);
    			        			
    		};
			
		};		
		
	};
	
})();