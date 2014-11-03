/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationAddSubjectCategoryController', IntraExtensionConfigurationAddSubjectCategoryController);
	
	IntraExtensionConfigurationAddSubjectCategoryController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationAddSubjectCategoryController($scope, $translate, alertService, intraExtensionService) {
		
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
        		
        		intraExtensionService.data.subject.subject.create({ie_uuid: add.intraExtension._id}, add.subject, createSuccess, createError);
        		        		        		
        	}	
			
			function createSuccess(data) {
    			
				add.subject.uuid = _.first(data.subjects);
				
    			$translate('moon.intraExtension.configure.subject.add.success', { subjectName: add.subject.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionSubjectCreatedSuccess', add.subject);
    			
    		};
    		
    		function createError(reason) {
    			
    			$translate('moon.intraExtension.configure.subject.add.error', { subjectName: add.subject.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionSubjectCreatedError', add.subject);
    			        			
    		};
			
		};		
		
	};
	
})();