/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationDeleteSubjectCategoryValueController', IntraExtensionConfigurationDeleteSubjectCategoryValueController);
	
	IntraExtensionConfigurationDeleteSubjectCategoryValueController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationDeleteSubjectCategoryValueController($scope, $translate, alertService, intraExtensionService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.intraExtension = $scope.intraExtension;
		del.category = $scope.category;
		del.value = $scope.value;
		
		del.remove = deleteValue;
		
		/*
		 * 
		 */
		
		function deleteValue() {
				
			intraExtensionService.data.subject.categoryValue.remove({ie_uuid: del.intraExtension._id, category: del.category.name, value: del.value}, deleteSuccess, deleteError);
			
			function deleteSuccess(data) {
				
				$translate('moon.intraExtension.configure.subject.categoryValue.remove.success', { valueName: del.value }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
				
				$scope.$emit('event:intraExtensionSubjectCategoryValueDeletedSuccess', { category: del.category, value: del.value });
				
			};
			
			function deleteError(reason) {
				
				$translate('moon.intraExtension.configure.subject.categoryValue.remove.error', { valueName: del.value }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
				
				$scope.$emit('event:intraExtensionSubjectCategoryValueDeletedError', { category: del.category, value: del.value });
				
			};
			
		};		
		
	};
	
})();