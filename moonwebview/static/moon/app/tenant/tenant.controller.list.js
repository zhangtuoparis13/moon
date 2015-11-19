/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('TenantListController', TenantListController);
	
	TenantListController.$inject = ['$rootScope', '$scope', '$filter', '$modal', '$translate', 'ngTableParams', 'alertService', 'intraExtensionService', 'tenants'];
	
	function TenantListController($rootScope, $scope, $filter, $modal, $translate, ngTableParams, alertService, intraExtensionService, tenants) {
		
		var list = this;
		
		/*
		 * 
		 */
		
		list.tenants = tenants;
		
		list.getTenants = getTenants;
		list.hasTenants = hasTenants;
		
		list.table = {};
		
		list.addTenant = addTenant;
		list.deleteTenant = deleteTenant;
		list.refreshTenants = refreshTenants;
		list.updateTenants = updateTenants;
		
		list.getMappedIntraExtensionName = getMappedIntraExtensionName;
		
		list.search = { query: '', 
						find: searchTenant, 
						reset: searchReset };
		
		list.add = { modal: $modal({ template: 'static/moon/app/tenant/tenant-add.tpl.html', show: false }), 
					 showModal: showAddModal };
		
		list.del = { modal: $modal({ template: 'static/moon/app/tenant/tenant-delete.tpl.html', show: false }), 
					 showModal: showDeleteModal };
		
		list.map = { modal: $modal({ template: 'static/moon/app/tenant/tenant-map.tpl.html', show: false }), 
					 showModal: showMapModal };
		
		list.unmap = { modal: $modal({ template: 'static/moon/app/tenant/tenant-unmap.tpl.html', show: false }), 
				 	   showModal: showUnmapModal };
		
		list.view = { modal: $modal({ template: 'static/moon/app/tenant/tenant-view.tpl.html', show: false }), 
			 	   	  showModal: showViewModal };
						
		newTenantsTable();
		// resolveMappedIntraExtensions();
		
		/*
		 * ---- events
		 */
		
		var rootListeners = {
				
				'event:tenantCreatedSuccess': $rootScope.$on('event:tenantCreatedSuccess', tenantCreatedSuccess),
				'event:tenantCreatedError': $rootScope.$on('event:tenantCreatedError', tenantCreatedError),
				
				'event:tenantDeletedSuccess': $rootScope.$on('event:tenantDeletedSuccess', tenantDeletedSuccess),
				'event:tenantDeletedError': $rootScope.$on('event:tenantDeletedError', tenantDeletedError),
				
				'event:tenantMappedSuccess': $rootScope.$on('event:tenantMappedSuccess', tenantMappedSuccess),
				'event:tenantMappedError': $rootScope.$on('event:tenantMappedError', tenantMappedError),
				
				'event:tenantUnmappedSuccess': $rootScope.$on('event:tenantUnmappedSuccess', tenantUnmappedSuccess),
				'event:tenantUnmappedError': $rootScope.$on('event:tenantUnmappedError', tenantUnmappedError)
				
		};
		
		for (var unbind in rootListeners) {
			  $scope.$on('$destroy', rootListeners[unbind]);
		}
		
		/*
		 * ---- resolve mapped intra-extensions
		 */
		
		function resolveMappedIntraExtensions() {
			
			_(list.tenants).each(function(aTenant) {
				
				aTenant.intraExtension = null;
				aTenant.extensionUuid = null;
				
				var extension = _(superExtensions.super_extensions).find(function(anExtension) {
					return anExtension.tenant_uuid === aTenant.uuid;
				});
				
				if(extension) {
					
					aTenant.extensionUuid = _.first(extension.intra_extension_uuids);
					
					intraExtensionService.findOne(aTenant.extensionUuid).then(function(intraExtension) {
						aTenant.intraExtension = intraExtension.intra_extensions;
					});
					
				}
				
			});
			
		};
		
		/*
		 * ---- table
		 */
		
		function hasTenants() {
			return list.getTenants().length > 0;
		}
				
		function getTenants() {
			 return list.tenants ? list.tenants : [];
		};
		
		function addTenant(tenant) {
			list.tenants.push(tenant);			
		};
		
		function deleteTenant(tenant) {
			list.tenants = _.chain(list.tenants).reject({uuid: tenant.uuid}).value();
		};
		
		function refreshTenants() {
			
			list.table.total(list.tenants.length);
			list.table.reload();
			
		};
		
		function updateTenants(tenant) {
			
			_(list.tenants).each(function(aTenant) {
        		if(aTenant.uuid === tenant.uuid) {
        			aTenant = _.clone(tenant); 
        		}
        	});
			
			return list.tenants;
			
		};
		
		function newTenantsTable() {
			
			list.table = new ngTableParams({
			    
				page: 1,            // show first page
				count: 10,          // count per page
				sorting: {
					name: 'asc' // initial sorting
				}
	   	
			}, {
		    	
				total: function () { return list.getTenants().length; }, // length of data
				getData: function($defer, params) {
		        	
					var orderedData = params.sorting() ? $filter('orderBy')(list.getTenants(), params.orderBy()) : list.getTenants();
					$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
		        	
				},
				$scope: { $data: {} }
		        
			});
			
			return list.table;
			
		};
		
		function getMappedIntraExtensionName(tenant) {
			return _.first(tenant.intraExtension.name);
		};
   			 
		/*
		 * ---- search
		 */
		 			    	
		function searchTenant(tenant){
		    
			if (tenant.name.indexOf(list.search.query) != -1 
					|| tenant.description.indexOf(list.search.query) != -1) {
				
		        return true;
		    
			}
		    
			return false;
		        
		};
		
		function searchReset() {
			list.search.query = '';
		};
		
		/*
		 * ---- add
		 */
		
		function showAddModal() {
        	list.add.modal.$promise.then(list.add.modal.show);
        };
                
        function tenantCreatedSuccess(event, tenant) {
        	
        	list.addTenant(tenant);
        	list.refreshTenants();
			
			list.add.modal.hide();
        	
        };
        
        function tenantCreatedError(event, tenant) {
        	list.add.modal.hide();
        };
        
        /*
         * ---- delete
         */
        
        function showDeleteModal(tenant) {
        	
        	list.del.modal.$scope.tenant = tenant;
        	list.del.modal.$promise.then(list.del.modal.show);
        	
        };
        
        function tenantDeletedSuccess(event, tenant) {
        	        	
        	list.deleteTenant(tenant);
        	list.refreshTenants();
			
			list.del.modal.hide();
        	
        };
        
        function tenantDeletedError(event, tenant) {
        	list.del.modal.hide();
        };
        
        /*
         * ---- map
         */
        
        function showMapModal(tenant) {
        	
        	list.map.modal.$scope.tenant = tenant;
        	list.map.modal.$promise.then(list.map.modal.show);
        	
        };
        
        function tenantMappedSuccess(event, tenant) {
        	
        	list.updateTenants(tenant);
			list.map.modal.hide();
			
        };
        
        function tenantMappedError(event, tenant) {
        	list.map.modal.hide();
        };
        
        /*
         * ---- unmap
         */
        
        function showUnmapModal(tenant) {
        	
        	list.unmap.modal.$scope.tenant = tenant;
        	list.unmap.modal.$promise.then(list.unmap.modal.show);
        	
        };
        
        function tenantUnmappedSuccess(event, tenant) {
        	
        	list.updateTenants(tenant);
        	list.unmap.modal.hide();
        	
        };
        
        function tenantUnmappedError(event, tenant) {
        	list.unmap.modal.hide();        	
        };
        
        /*
         * ---- view
         */
        
        function showViewModal(tenant) {
        	
        	list.view.modal.$scope.tenant = tenant;
        	list.view.modal.$promise.then(list.view.modal.show);
        	
        };
		
	};
	
})();
