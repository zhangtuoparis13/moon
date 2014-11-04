/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationAddObjectController', IntraExtensionConfigurationAddObjectController);
	
	IntraExtensionConfigurationAddObjectController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService', 'novaService'];
	
	function IntraExtensionConfigurationAddObjectController($scope, $translate, alertService, intraExtensionService, novaService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.form = {};
		add.intraExtension = $scope.intraExtension;
		add.object = { name: '', image: '', flavor: '' };
		
		add.images  =[];
		add.imagesLoading = true;
		
		add.flavors = [];
		add.flavorsLoading = true;
		
		add.create = addObject;
		
		resolveImages();
		resolveFlavors();
		
		/*
		 * 
		 */
		
		function resolveImages() {
			
			return novaService.data.image.query().$promise.then(function(data) {
				
				add.images = data.images;
				add.imagesLoading = false;
				
				return add.images;
				
			});
			
		};
		
		function resolveFlavors() {
			
			return novaService.data.flavor.query().$promise.then(function(data) {
				
				add.flavors = data.flavors;
				add.flavorsLoading = false;
				
				return add.flavors;
				
			});
			
		};
		
		/*
		 * 
		 */
		
		function addObject() {
			
			if(add.form.$invalid) {
            	
	        	if(add.form.name.$pristine && add.form.name.$invalid) {
	    			
	        		add.form.name.$dirty = true;
	        		add.form.name.$setValidity('required', false);
	    			
	    		} 
	        	
	        	if(add.form.image.$pristine && add.form.image.$invalid) {
	    			
	        		add.form.image.$dirty = true;
	        		add.form.image.$setValidity('required', false);
	    			
	    		}
	        	
	        	if(add.form.flavor.$pristine && add.form.flavor.$invalid) {
	    			
	        		add.form.flavor.$dirty = true;
	        		add.form.flavor.$setValidity('required', false);
	    			
	    		}

        	} else {
        		
        		var payload = { name: add.object.name, image_name: add.object.image.name, flavor_name: add.object.flavor.name };
        		
        		intraExtensionService.data.object.object.create({ie_uuid: add.intraExtension._id}, payload, createSuccess, createError);
        		        		        		
        	}	
			
			function createSuccess(data) {
    			
				add.object.uuid = _.first(data.objects);
				
    			$translate('moon.intraExtension.configure.object.add.success', { objectName: add.object.name }).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionObjectCreatedSuccess', add.object);
    			
    		};
    		
    		function createError(reason) {
    			
    			$translate('moon.intraExtension.configure.object.add.error', { objectName: add.object.name }).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
    			
    			$scope.$emit('event:intraExtensionObjectCreatedError');
    			        			
    		};
			
		};		
		
	};
	
})();