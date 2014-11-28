/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationDeleteSubjectController', IntraExtensionConfigurationDeleteSubjectController);
	
	IntraExtensionConfigurationDeleteSubjectController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationDeleteSubjectController($scope, $translate, alertService, intraExtensionService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.intraExtension = $scope.intraExtension;
		del.subject = $scope.subject;
		del.remove = deleteSubject;
		
		/*
		 * 
		 */
		
		function deleteSubject() {
				
			intraExtensionService.data.subject.subject.remove({ie_uuid: del.intraExtension._id, subject_uuid: del.subject.uuid}, deleteSuccess, deleteError);
			
			function deleteSuccess(data) {
				
				$translate('moon.intraExtension.configure.subject.remove.success', { subjectName: del.subject.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
				
				$scope.$emit('event:intraExtensionSubjectDeletedSuccess', del.subject);
				
			};
			
			function deleteError(reason) {
				
				$translate('moon.intraExtension.configure.subject.remove.error', { subjectName: del.subject.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
				
				$scope.$emit('event:intraExtensionSubjectDeletedError', del.subject);
				
			};
			
		};		
		
	};
	
})();