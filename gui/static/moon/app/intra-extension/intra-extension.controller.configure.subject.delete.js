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
		del.remove = deleteSubject;
		
		/*
		 * 
		 */
		
		function deleteSubject(intraExtension, subject) {
				
			// TODO
			
		};		
		
	};
	
})();