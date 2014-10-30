/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('TenantDeleteController', TenantDeleteController);
	
	TenantDeleteController.$inject = ['$scope', '$translate', 'alertService', 'tenantService'];
	
	function TenantDeleteController($scope, $translate, alertService, tenantService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.tenant = $scope.tenant;
		del.remove = deleteTenant;
		
		/*
		 * ---- delete
		 */
		
		function deleteTenant(tenant) {
        	
			tenantService.data.tenant.remove({project_uuid: tenant.uuid}, deleteSuccess, deleteError);
			
			function deleteSuccess(data) {
        		
        		$translate('moon.tenant.remove.success', { tenantName: tenant.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
        		
        		$scope.$emit('event:tenantDeletedSuccess', tenant);
        		
        	};
        	
        	function deleteError(reason) {
        		
        		$translate('moon.tenant.remove.error', { tenantName: tenant.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
        		
        		$scope.$emit('event:tenantDeletedError', tenant);
        		
        	};
        	        	
        };
		
	};
	
})();
