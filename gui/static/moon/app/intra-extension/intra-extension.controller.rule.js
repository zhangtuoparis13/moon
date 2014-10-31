/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionRuleController', IntraExtensionRuleController);
	
	IntraExtensionRuleController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionRuleController($scope, $translate, alertService, intraExtensionService) {
		
		var rule = this;
		
		
	};
	
})();