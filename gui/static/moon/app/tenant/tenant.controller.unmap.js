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
		
		function unmapTenant() {
			
			var mapping = {tenant_uuid: unmap.tenant.uuid, intra_extension_uuid: unmap.tenant.intraExtension._id};
    		
        	tenantService.data.map.remove(mapping, mapping, unmapSuccess, unmapError);
        	
        	function unmapSuccess(data) {
        		
        		$translate('moon.tenant.unmap.success', { tenantName: unmap.tenant.name, intraExtensionName: _.first(unmap.tenant.intraExtension.name) }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });
        		
        		unmap.tenant.extensionUuid = null;
        		unmap.tenant.intraExtension= null;
        		
        		$scope.$emit('event:tenantUnmappedSuccess', unmap.tenant);
        		
        	};
        	
        	function unmapError(reason) {
        		
        		$translate('moon.tenant.unmap.error', { tenantName: unmap.tenant.name, intraExtensionName: _.first(unmap.tenant.intraExtension.name) }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });
        		
        		$scope.$emit('event:tenantUnmappedError', unmap.tenant);
        		
        	};
			
		};
		
	};
			
})();
