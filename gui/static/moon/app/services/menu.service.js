/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.factory('menuService', menuService)
	
	menuService.$inject = ['$state'];
	
	function menuService($state) {
		
		var service = { 
				isTenantTabActive: isTenantTabActive,
				isIntraExtensionTabActive: isIntraExtensionTabActive,
				isInterExtensionTabActive: isInterExtensionTabActive
		};
		
		return service;
		
		function isTenantTabActive() {
			return $state.includes('moon.tenant');
		};
			
		function isIntraExtensionTabActive() {
			return $state.includes('moon.intraExtension');
		};
		
		function isInterExtensionTabActive() {
			return $state.includes('moon.interExtension');
		};
		
	};
	
})();
