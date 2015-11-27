/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('TenantMapController', TenantMapController);
	
	TenantMapController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'tenantService', 'intraExtensionService'];
	
	function TenantMapController($scope, $translate, alertService, formService, tenantService, intraExtensionService) {

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
				
				/* Filtering:
				 * --> Invalid intraExtnesion
				 * --> non-free intraextensions
				 */
				map.intraExtensions = _(data).filter(function(intraExtension) {
					return intraExtension.id != null;
				}).filter(function(intraExtension) {
					return intraExtension.tenant_uuid == "" || intraExtension.tenant_uuid == null;
				});
				
				map.intraExtensionsLoading = false;
			console.log(JSON.stringify(map.intraExtensions));	
				return map.intraExtensions;
				
			});
			
		};
		
		function mapTenant() {
			
			if(formService.isInvalid(map.form)) {
        		
        		formService.checkFieldsValidity(map.form);
        	        	
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
