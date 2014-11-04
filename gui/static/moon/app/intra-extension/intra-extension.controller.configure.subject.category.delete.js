/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationDeleteSubjectCategoryController', IntraExtensionConfigurationDeleteSubjectCategoryController);
	
	IntraExtensionConfigurationDeleteSubjectCategoryController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationDeleteSubjectCategoryController($scope, $translate, alertService, intraExtensionService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.intraExtension = $scope.intraExtension;
		del.category = $scope.category;
		del.remove = deleteCategory;
		
		/*
		 * 
		 */
		
		function deleteCategory() {
				
			intraExtensionService.data.subject.category.remove({ie_uuid: del.intraExtension._id, category_name: del.category.name}, deleteSuccess, deleteError);
			
			function deleteSuccess(data) {
				
				$translate('moon.intraExtension.configure.subject.category.remove.success', { categoryName: del.category.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
				
				$scope.$emit('event:intraExtensionSubjectCategoryDeletedSuccess', del.category);
				
			};
			
			function deleteError(reason) {
				
				$translate('moon.intraExtension.configure.subject.category.remove.error', { categoryName: del.category.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
				
				$scope.$emit('event:intraExtensionSubjectCategoryDeletedError', del.category);
				
			};
			
		};		
		
	};
	
})();