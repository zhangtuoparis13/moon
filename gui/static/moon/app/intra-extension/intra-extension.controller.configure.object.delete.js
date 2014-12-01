/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationDeleteObjectController', IntraExtensionConfigurationDeleteObjectController);
	
	IntraExtensionConfigurationDeleteObjectController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionConfigurationDeleteObjectController($scope, $translate, alertService, intraExtensionService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.intraExtension = $scope.intraExtension;
		del.object = $scope.object;
		del.remove = deleteObject;
		
		/*
		 * 
		 */
		
		function deleteObject() {
				
			intraExtensionService.data.object.object.remove({ie_uuid: del.intraExtension._id, object_uuid: del.object.uuid}, deleteSuccess, deleteError);
			
			function deleteSuccess(data) {
				
				$translate('moon.intraExtension.configure.object.remove.success', { objectName: del.object.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
				
				$scope.$emit('event:intraExtensionObjectDeletedSuccess', del.object);
				
			};
			
			function deleteError(reason) {
				
				$translate('moon.intraExtension.configure.object.remove.error', { objectName: del.object.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
				
				$scope.$emit('event:intraExtensionObjectDeletedError', del.object);
				
			};
			
		};		
		
	};
	
})();