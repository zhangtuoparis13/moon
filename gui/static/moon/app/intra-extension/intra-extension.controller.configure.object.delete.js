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
		
		function deleteObject(intraExtension, object) {
				
			// TODO
			
		};		
		
	};
	
})();