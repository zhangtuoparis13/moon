/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('TenantAddController', TenantAddController);
	
	TenantAddController.$inject = ['$scope', '$translate', 'alertService', 'formService', 'tenantService', 'DEFAULT_CST'];
	
	function TenantAddController($scope, $translate, alertService, formService, tenantService, DEFAULT_CST) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		//@tofo: verifier si l'arg enable est prise en compte server-side
		add.tenant = { tenant_name: null, tenant_description: null, enabled: true, domain: DEFAULT_CST.DOMAIN.DEFAULT };
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
        		
			//@ todo: clarify projects notions
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
