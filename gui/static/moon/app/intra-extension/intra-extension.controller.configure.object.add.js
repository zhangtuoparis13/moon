/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationAddObjectController', IntraExtensionConfigurationAddObjectController);
	
	IntraExtensionConfigurationAddObjectController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationAddObjectController($scope, $translate, alertService, intraExtensionService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		add.intraExtension = $scope.intraExtension;
		add.object = { name: '', image: '', flavor: '' };
		
		add.create = addObject;
		
		/*
		 * 
		 */
		
		function addObject(intraExtension, object) {
			
			if(add.form.$invalid) {
            	
	        	if(add.form.name.$pristine && add.form.name.$invalid) {
	    			
	        		add.form.name.$dirty = true;
	        		add.form.name.$setValidity('required', false);
	    			
	    		} 
	        	
	        	if(add.form.image.$pristine && add.form.image.$invalid) {
	    			
	        		add.form.image.$dirty = true;
	        		add.form.image.$setValidity('required', false);
	    			
	    		}
	        	
	        	if(add.form.flavor.$pristine && add.form.flavor.$invalid) {
	    			
	        		add.form.flavor.$dirty = true;
	        		add.form.flavor.$setValidity('required', false);
	    			
	    		}

        	} else {
        		
        		// TODO
        		intraExtensionService.data.object.create({ie_uuid: intraExtension._id}, object, createSuccess, createError);
        		        		        		
        	}	
			
			function createSuccess(data) {
    			
    			$translate('moon.intraExtension.configure.object.add.success', { objectName: object.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionObjectCreatedSuccess', object);
    			
    		};
    		
    		function createError(reason) {
    			
    			$translate('moon.intraExtension.configure.object.add.error', { objectName: object.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionObjectCreatedError', object);
    			        			
    		};
			
		};		
		
	};
	
})();