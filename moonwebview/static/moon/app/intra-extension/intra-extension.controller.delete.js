/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionDeleteController', IntraExtensionDeleteController);
	
	IntraExtensionDeleteController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionDeleteController($scope, $translate, alertService, intraExtensionService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.intraExtension = $scope.intraExtension;
		del.remove = deleteIntraExtension;
		
		/*
		 * 
		 */
		
		function deleteIntraExtension() {
			
			intraExtensionService.data.intraExtension.remove({ie_uuid: del.intraExtension._id}, deleteSuccess, deleteError);
			
			function deleteSuccess(data) {
				
				$translate('moon.intraExtension.remove.success', { intraExtensionName: _.first(del.intraExtension.name) }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
				
				$scope.$emit('event:intraExtensionDeletedSuccess', del.intraExtension);
				
			};
			
			function deleteError(reason) {
				
				$translate('moon.intraExtension.remove.error', { intraExtensionName: _.first(del.intraExtension.name) }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
				
				$scope.$emit('event:intraExtensionDeletedError', del.intraExtension);
				
			};
			
		};
		
	};
	
})();