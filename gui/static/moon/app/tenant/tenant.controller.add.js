/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('TenantAddController', TenantAddController);
	
	TenantAddController.$inject = ['$scope', '$translate', 'alertService', 'tenantService'];
	
	function TenantAddController($scope, $translate, alertService, tenantService) {
		
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
        	
        	if(add.form.$invalid) {
        	
	        	if(add.form.name.$pristine && add.form.name.$invalid) {
	    			
	        		add.form.name.$dirty = true;
	        		add.form.name.$setValidity('required', false);
	    			
	    		} 
	        	
	        	if(add.form.domain.$pristine && add.form.domain.$invalid) {
	    			
	        		add.form.domain.$dirty = true;
	        		add.form.domain.$setValidity('required', false);
	    			
	    		}
        	
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
