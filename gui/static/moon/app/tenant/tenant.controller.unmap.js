/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('TenantUnmapController', TenantUnmapController);
	
	TenantUnmapController.$inject = ['$scope', '$translate', 'alertService', 'tenantService'];
	
	function TenantUnmapController($scope, $translate, alertService, tenantService) {

		var unmap = this;
		
		/*
		 * 
		 */
		
		unmap.tenant = $scope.tenant;
		unmap.unmap = unmapTenant;
		
		/*
		 * 
		 */
		
		function unmapTenant(tenant) {
			
			var mapping = {tenant_uuid: tenant.uuid, intra_extension_uuid: tenant.intraExtension._id};
    		
        	tenantService.data.map.remove(mapping, mapping, unmapSuccess, unmapError);
        	
        	function unmapSuccess(data) {
        		
        		$translate('moon.tenant.unmap.success', { tenantName: tenant.name, intraExtensionName: _.first(tenant.intraExtension.name) }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });
        		
        		tenant.extensionUuid = null;
        		tenant.intraExtension= null;
        		
        		$scope.$emit('event:tenantUnmappedSuccess', tenant);
        		
        	};
        	
        	function unmapError(reason) {
        		
        		$translate('moon.tenant.unmap.error', { tenantName: tenant.name, intraExtensionName: _.first(tenant.intraExtension.name) }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
        		
        		$scope.$emit('event:tenantUnmappedError', tenant);
        		
        	};
			
		};
		
	};
			
})();
