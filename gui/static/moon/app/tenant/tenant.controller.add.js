/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('TenantAddController', TenantAddController);
	
	TenantAddController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'tenantService'];
	
	function TenantAddController($scope, $translate, alertService, formService, tenantService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		add.tenant = { name: null, description: null, enabled: true, domain: 'Default'};
		add.create= createTenant;
		
		/*
		 * ---- create
		 */
		
		function createTenant() {
        	
        	if(formService.isInvalid(add.form)) {
        		
        		formService.checkFieldsValidity(add.form);
        	        	
        	} else {
        	
	        	tenantService.data.tenant.create({}, add.tenant, createSuccess, createError);

    		}
        	
        	function createSuccess(data) {
        		
        		var created = _(data.projects).find(function(aTenant) {
        			return add.tenant.name === aTenant.name;
        		});
        		
        		$translate('moon.tenant.add.success', { tenantName: created.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
        		
        		$scope.$emit('event:tenantCreatedSuccess', created);	
        			        		
        	};
        	
        	function createError(reason) {
        		
        		$translate('moon.tenant.add.error', { tenantName: add.tenant.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
        		
        		$scope.$emit('event:tenantCreatedError', add.tenant);
        		
        	};
        	
        };
		
	};
	
})();
