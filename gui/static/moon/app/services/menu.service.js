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
			return $state.is('moon.tenant');
		};
			
		function isIntraExtensionTabActive() {
			return $state.is('moon.intraExtension') || $state.is('moon.intraExtensionConfiguration');
		};
		
		function isInterExtensionTabActive() {
			return $state.is('moon.interExtension');
		};
		
	};
	
})();
