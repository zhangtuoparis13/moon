/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionListController', IntraExtensionListController);
	
	IntraExtensionListController.$inject = ['$q', '$rootScope', '$scope', '$filter', '$modal', '$translate', 'ngTableParams', 'alertService', 'intraExtensionService', 'tenantService', 'intraExtensions'];

	function IntraExtensionListController($q, $rootScope, $scope, $filter, $modal, $translate, ngTableParams, alertService, intraExtensionService, tenantService, intraExtensions) {
		
		var list = this;
		
		/*
		 * 
		 */
		
		list.intraExtensions = intraExtensions;
		
		list.getIntraExtensions = getIntraExtensions;
		list.hasIntraExtensions = hasIntraExtensions;
		list.getIntraExtensionName = getIntraExtensionName;
		list.hasMappedTenant = hasMappedTenant;
		
		list.table = {};
		
		list.addIntraExtension = addIntraExtension;
		list.deleteIntraExtension = deleteIntraExtension;
		list.refreshIntraExtensions = refreshIntraExtensions;
		list.updateIntraExtensions = updateIntraExtensions;
		
		list.getMappedTenantName = getMappedTenantName;
		
		list.search = { query: '', 
						find: searchIntraExtension, 
						reset: searchReset };
		
		list.add = { modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-add.tpl.html', show: false }), 
				 	 showModal: showAddModal };
		
		list.del = { modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-delete.tpl.html', show: false }), 
				 	 showModal: showDeleteModal };
		
		newIntraExtensionsTable();
		resolveMappedTenants();
		
		/*
		 * ---- events
		 */
		
		var rootListeners = {
				
				'event:intraExtensionCreatedSuccess': $rootScope.$on('event:intraExtensionCreatedSuccess', intraExtensionCreatedSuccess),
				'event:intraExtensionCreatedError': $rootScope.$on('event:intraExtensionCreatedError', intraExtensionCreatedError),
				
				'event:intraExtensionDeletedSuccess': $rootScope.$on('event:intraExtensionDeletedSuccess', intraExtensionDeletedSuccess),
				'event:intraExtensionDeletedError': $rootScope.$on('event:intraExtensionDeletedError', intraExtensionDeletedError),
				
		};
		
		for (var unbind in rootListeners) {
			  $scope.$on('$destroy', rootListeners[unbind]);
		}
		
		/*
		 * 
		 */
		
		function getIntraExtensions() {
			return (list.intraExtensions) ? list.intraExtensions : [];
		};
		
		function hasIntraExtensions() {
			return list.getIntraExtensions().length > 0;
		};
		
		function addIntraExtension(intraExtension) {
			list.intraExtensions.push(intraExtension);			
		};
		
		function deleteIntraExtension(intraExtension) {
			list.intraExtensions = _.chain(list.intraExtensions).reject({_id: intraExtension._id}).value();
		};
		
		function refreshIntraExtensions() {
			
			list.table.total(list.intraExtensions.length);
			list.table.reload();
						
		};
		
		function updateIntraExtensions(intraExtension) {
			
			_(list.intraExtensions).each(function(anIntraExtension) {
        		if(anIntraExtension._id === intraExtension._id) {
        			anIntraExtension = _.clone(intraExtension); 
        		}
        	});
			
			return list.intraExtensions;
			
		};
		
		function getMappedTenantName(intraExtension) {
			return intraExtension.tenant.name;
		};

		function getIntraExtensionName(intraExtension) {
			return _.first(intraExtension.name);
		};

		function hasMappedTenant(intraExtension) {
			return intraExtension.tenant_uuid != "" && intraExtension.tenant_uuid != null;
		};
		
		function newIntraExtensionsTable() {
			
			list.table = new ngTableParams({
			    
				page: 1,            // show first page
				count: 10,          // count per page
				sorting: {
					_id: 'asc' // initial sorting
				}
	   	
			}, {
		    	
				total: function () { return list.getIntraExtensions().length; }, // length of data
				getData: function($defer, params) {
		        	
					var orderedData = params.sorting() ? $filter('orderBy')(list.getIntraExtensions(), params.orderBy()) : list.getIntraExtensions();
					$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
		        	
				},
				$scope: { $data: {} }
		        
			});
			
			return list.table;
			
		};
		
		/*
		 * 
		 */
		
		function resolveMappedTenants() {
			
			_(list.intraExtensions).each(function(anIntraExtension) {
				
				anIntraExtension.tenant = null;
				
				if(anIntraExtension.tenant_uuid) {
					
					tenantService.findOne(anIntraExtension.tenant_uuid).then(function(tenant) {
						anIntraExtension.tenant = _.first(tenant.projects);
					});
					
				}
				
			});
			
		};
		
		/*
		 * --- search
		 */
		
		function searchIntraExtension(intraExtension){
		    
			if (list.getIntraExtensionName(intraExtension).indexOf(list.search.query) != -1 
					|| intraExtension.authz.metadata.model.indexOf(list.search.query) != -1) {
				
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
                
        function intraExtensionCreatedSuccess(event, intraExtension) {
        	
        	list.addIntraExtension(intraExtension);
        	list.refreshIntraExtensions();
			
			list.add.modal.hide();
        	
        };
        
        function intraExtensionCreatedError(event, intraExtension) {
        	list.add.modal.hide();
        };
        
        /*
         * ---- delete
         */
        
        function showDeleteModal(intraExtension) {
        	
        	list.del.modal.$scope.intraExtension = intraExtension;
        	list.del.modal.$promise.then(list.del.modal.show);
        	
        };
        
        function intraExtensionDeletedSuccess(event, intraExtension) {
        	        	
        	list.deleteIntraExtension(intraExtension);
        	list.refreshIntraExtensions();
			
			list.del.modal.hide();
        	
        };
        
        function intraExtensionDeletedError() {
        	list.del.modal.hide();
        };
		
	};
		
})();
