/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
	
	angular
		.module('moon')
				.controller('HeaderController', HeaderController)
	
	HeaderController.$inject = ['$rootScope', '$state', '$translate'];
	
	function HeaderController($rootScope, $state, $translate) {
				    
		this.$state = $state;
		
    	$rootScope.changeLocale = function(localeKey, event) {
			
            event.preventDefault();
            
            $translate.use(localeKey);
            $translate.preferredLanguage(localeKey);
                            
        };
		
	};
	
})();