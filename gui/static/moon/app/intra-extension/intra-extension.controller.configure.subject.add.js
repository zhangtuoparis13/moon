/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationAddSubjectController', IntraExtensionConfigurationAddSubjectController);
	
	IntraExtensionConfigurationAddSubjectController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'intraExtensionService', 'DEFAULT_CST'];
	
	function IntraExtensionConfigurationAddSubjectController($scope, $translate, alertService, formService, intraExtensionService, DEFAULT_CST) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		add.intraExtension = $scope.intraExtension;
		add.subject = { name: '', domain: DEFAULT_CST.DOMAIN.DEFAULT, enabled: true, project: add.intraExtension.tenant.uuid, password: '', description: '' };
		
		add.create = addSubject;
		
		/*
		 * 
		 */
		
		function addSubject() {
			
			if(formService.isInvalid(add.form)) {
        		
        		formService.checkFieldsValidity(add.form);
        	        	
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