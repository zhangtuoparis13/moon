/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('TenantMapController', TenantMapController);
	
	TenantMapController.$inject = ['$scope', '$translate', 'alertService', 'tenantService', 'intraExtensionService'];
	
	function TenantMapController($scope, $translate, alertService, tenantService, intraExtensionService) {

		var map = this;
		
		/*
		 * 
		 */
		
		map.form = {};
		
		map.tenant = $scope.tenant;
		
		map.intraExtensions = [];
		map.intraExtensionsLoading = true;
		
		map.selectedIntraExtension = null;
		
		map.map = mapTenant;
				
		resolveIntraExtensions();
		
		/*
		 * 
		 */
		
		function resolveIntraExtensions() {
			
			intraExtensionService.findAll().then(function(data) {
				
				map.intraExtensions = _(data).filter(function(intraExtension) {
					return intraExtension.tenant_uuid == "" || intraExtension.tenant_uuid == null;
				});
				
				map.intraExtensionsLoading = false;
				
				return map.intraExtensions;
				
			});
			
		};
		
		function mapTenant() {
			
			if(map.form.$invalid) {
	        	
	        	if(map.form.intraExtension.$pristine &&map.form.intraExtension.$invalid) {
	    			
	        		map.form.intraExtension.$dirty = true;
	        		map.form.intraExtension.$setValidity('required', false);
	    			
	    		} 
	        	        	
        	} else {
        	
        		var mapping = {tenant_uuid: map.tenant.uuid, intra_extension_uuid: map.selectedIntraExtension._id};
        		
	        	tenantService.data.map.create(mapping, mapping, mapSuccess, mapError);
	        		        		        	        	
    		}
			
			function mapSuccess(data) {
        		
				map.tenant.extensionUuid = map.selectedIntraExtension._id;
				map.tenant.intraExtension = map.selectedIntraExtension;
        		
        		$translate('moon.tenant.map.success', { tenantName: map.tenant.name, intraExtensionName: _.first(map.selectedIntraExtension.name) }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
        		
        		$scope.$emit('event:tenantMappedSuccess', map.tenant);
        		
        	};
        	
        	function mapError(response) {
        		
        		$translate('moon.tenant.map.error', { tenantName: map.tenant.name, intraExtensionName: _.first(map.selectedIntraExtension.name) }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
        		
        		$scope.$emit('event:tenantMappedError', map.tenant);
        		
        	};
			
		};
		
	};
	
})();
