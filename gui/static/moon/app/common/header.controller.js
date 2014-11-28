/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.controller('HeaderController', HeaderController)
	
	HeaderController.$inject = ['$translate', 'menuService'];
	
	function HeaderController($translate, menuService) {
				 
		var header = this;
		
		/*
		 * 
		 */
		
		header.isTenantTabActive = menuService.isTenantTabActive;
		header.isIntraExtensionTabActive = menuService.isIntraExtensionTabActive;
		header.isInterExtensionTabActive = menuService.isInterExtensionTabActive;
		
		header.changeLocale = changeLocale; 
		
		/*
		 * 
		 */
		
		function changeLocale(localeKey, event) {
			
            event.preventDefault();
            
            $translate.use(localeKey);
            $translate.preferredLanguage(localeKey);
                            
        };
		
	};
	
})();