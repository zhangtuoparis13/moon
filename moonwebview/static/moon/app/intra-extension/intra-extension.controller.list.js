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
		list.getTenantFromIntraExtension = getTenantFromIntraExtension;
		list.getidFromIntraExtension = getidFromIntraExtension;
		
		list.table = {};
		
		list.addIntraExtension = addIntraExtension;
		list.deleteIntraExtension = deleteIntraExtension;
		list.refreshIntraExtensions = refreshIntraExtensions;
		list.updateIntraExtensions = updateIntraExtensions;
		
		list.getMappedTenantName = getMappedTenantName;
		list.getModelFromIntraExtension = getModelFromIntraExtension;
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
		
		/**
		 * Function getting an array of intraEtnesion JSON
		 * @return An array of valid intraextension.
		 */
		function getIntraExtensions() {
			if (!list.intraExtensions)
				return [];
			var result = [];
			var i;

			for (i in list.intraExtensions) {
				if (list.intraExtensions[i].id)
					result.push(list.intraExtensions[i]);
			}
			console.log(JSON.stringify(result));
			return result;
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
			
			_(_.values(list.intraExtensions)).each(function(anIntraExtension) {
        		if(anIntraExtension._id === intraExtension._id) {
					//@todo: Determine what this code should have been designed to do
        			anIntraExtension = _.clone(intraExtension); 
        		}
        	});
			
			return list.intraExtensions;
			
		};

		/**
		 * Get the id from an Intra Extension
		 * @param intraExtension The inspected intra-extension
		 * @returns {*} Its UUID
		 */
		function getidFromIntraExtension(intraExtension) {
			return intraExtension.id;
		};
		
		function getMappedTenantName(intraExtension) {
			return intraExtension.tenant.name;
		};

		/**
		 * Get the name of the Intra-Extension
		 * @param intraExtension The IntraExtension to inspect
		 * @returns {*} Its name.
		 */
		function getIntraExtensionName(intraExtension) {
			return (intraExtension) ? intraExtension.name : "";
		};

		function hasMappedTenant(intraExtension) {
			return intraExtension.tenant_uuid != "" && intraExtension.tenant_uuid != null;
		};

		/**
		 * Get a tenant from an intra-extension
		 * @param intraExtension An intra extension
		 * @returns {*|null|resolve.tenant|Function} The requiered tenant object
		 */
		function getTenantFromIntraExtension(intraExtension) {
			return (intraExtension) ? intraExtension.tenant : null;
		}

		/**
		 * Generate a table item, directly usable by the rendering engine
		 * @returns {{}|*} the table
		 */
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
		
		/**
		 * Do the mapping between Intraextension Obkect and their tenant.
		 */
		function resolveMappedTenants() {
			return; // @todo: to be reimplemented

			// For each intra extension in in intraextension list,
			/* _(list.getIntraExtensions()).each(function(anIntraExtension) {
				// We reset to null the tenant,
				_.first(anIntraExtension).tenant = null;
				// If a tenant (uu)id is correctly specified,
				if(_.first(anIntraExtension).tenant_uuid) {
					// We ask the tenant service to get the corresponding tenant
					tenantService.findOne(_.first(anIntraExtension).tenant_uuid).then(function(tenant) {
							_.first(anIntraExtension).tenant = tenant;//.projects
					}
				);
				}
			});*/
		};
		
		/*
		 * --- search
		 */

		/**
		 * Indicate if an intra-extension having a specified name exists
		 * @param intraExtension Searched name
		 * @returns {boolean} True if a corresponding intra-extension is found, false otherwise
		 */
		function searchIntraExtension(intraExtension){
			if (list.getIntraExtensionName(intraExtension).indexOf(list.search.query) != -1
					|| intraExtension.authz.metadata.model.indexOf(list.search.query) != -1) {
		        return true;
			}
			return false;
		        
		};

		/**
		 * Retrieve the model name from an Intra extension
		 * @param intraextension Value of intra-extension
		 * @return A string containing the name of the associated model
		 */
		function getModelFromIntraExtension(intraextension){
			//Reinegrate authz in intraext.
			return (intraextension.authz) ? intraextension.authz.metadata.model : null;
		}

		/**
		 * Blank the search field
		 */
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
