/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationDeleteObjectCategoryValueController', IntraExtensionConfigurationDeleteObjectCategoryValueController);
	
	IntraExtensionConfigurationDeleteObjectCategoryValueController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationDeleteObjectCategoryValueController($scope, $translate, alertService, intraExtensionService) {
		
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
				
			intraExtensionService.data.object.categoryValue.remove({ie_uuid: del.intraExtension._id, category: del.category.name, value: del.value}, deleteSuccess, deleteError);
			
			function deleteSuccess(data) {
				
				$translate('moon.intraExtension.configure.object.categoryValue.remove.success', { valueName: del.value }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
				
				$scope.$emit('event:intraExtensionObjectCategoryValueDeletedSuccess', { category: del.category, value: del.value });
				
			};
			
			function deleteError(reason) {
				
				$translate('moon.intraExtension.configure.object.categoryValue.remove.error', { valueName: del.value }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
				
				$scope.$emit('event:intraExtensionObjectCategoryValueDeletedError', { category: del.category, value: del.value });
				
			};
			
		};		
		
	};
	
})();