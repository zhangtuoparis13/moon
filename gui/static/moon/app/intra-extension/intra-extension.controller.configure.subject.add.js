/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationAddSubjectController', IntraExtensionConfigurationAddSubjectController);
	
	IntraExtensionConfigurationAddSubjectController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationAddSubjectController($scope, $translate, alertService, intraExtensionService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		add.intraExtension = $scope.intraExtension;
		add.subject = { name: '', domain: 'Default', enabled: true, project: add.intraExtension.tenant.uuid, password: '', description: '' };
		
		add.create = addSubject;
		
		/*
		 * 
		 */
		
		function addSubject() {
			
			if(add.form.$invalid) {
            	
	        	if(add.form.name.$pristine && add.form.name.$invalid) {
	    			
	        		add.form.name.$dirty = true;
	        		add.form.name.$setValidity('required', false);
	    			
	    		} 
	        	
	        	if(add.form.domain.$pristine && add.form.domain.$invalid) {
	    			
	        		add.form.domain.$dirty = true;
	        		add.form.domain.$setValidity('required', false);
	    			
	    		}

				if(add.form.password.$pristine && add.form.password.$invalid) {
					
					add.form.password.$dirty = true;
					add.form.password.$setValidity('required', false);
					
				}
        	
        	} else {
        		
        		// TODO
        		intraExtensionService.data.subject.create({ie_uuid: add.intraExtension._id}, add.subject, createSuccess, createError);
        		        		        		
        	}	
			
			function createSuccess(data) {
    			
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