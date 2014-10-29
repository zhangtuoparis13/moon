/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationController', IntraExtensionConfigurationController);
	
	IntraExtensionConfigurationController.$inject = ['$q', '$rootScope', '$scope', '$translate', '$modal', 'alertService', 'tenantService', 'intraExtensionService', 'intraExtension', 'subjects', 'objects'];
	
	function IntraExtensionConfigurationController($q, $rootScope, $scope, $translate, $modal, alertService, tenantService, intraExtensionService, intraExtension, subjects, objects) {
		
		var conf = this;
		
		/*
		 * 
		 */
		
		conf.intraExtension = intraExtension.intra_extensions;
		
		conf.subject = { 
				subjects: [],
				subjectCategories: [],
				selectedSubjects: [],
				selectedCategories: [],
				add: { 
					modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-add.tpl.html', show: false }), 
				 	showModal: showSubjectAddModal
				},
				del: { 
					modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-delete.tpl.html', show: false }), 
				 	showModal: showSubjectDeleteModal
				}
		};
		
		
		conf.object = { 
				objects: [],
				objectCategories: [],
				selectedObjects: [],
				selectedCategories: [], 
				add: {
					modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-add.tpl.html', show: false }), 
		 	 	 	showModal: showObjectAddModal
				},
				del: {
					modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-delete.tpl.html', show: false }), 
		 	 	 	showModal: showObjectDeleteModal
				}
		};
				
		resolveSubjects(subjects);
		resolveObjects(objects);
		
		/*
		 * events
		 */
		
		var rootListeners = {
				
				'event:intraExtensionSubjectCreatedSuccess': $rootScope.$on('event:intraExtensionSubjectCreatedSuccess', intraExtensionSubjectCreatedSuccess),
				'event:intraExtensionSubjectCreatedError': $rootScope.$on('event:intraExtensionSubjectCreatedError', intraExtensionSubjectCreatedError)
				
		};
		
		for (var unbind in rootListeners) {
			  $scope.$on('$destroy', rootListeners[unbind]);
		}
		
		/*
		 * 
		 */
		
		function resolveSubjects(subjects) {
			
			var promises = [];
			
			_(subjects.subjects).each(function(subjectId) {
				promises.push(tenantService.data.subject.get({ project_uuid: conf.intraExtension.tenant_uuid, user_uuid: subjectId }).$promise);
			});
			
			return $q.all(promises).then(function(data) {
				
				conf.subject.subjects = _(data).map(function(aSubject){
					return _.first(aSubject.users);
				});
				
				conf.subject.subjects = _(conf.subject.subjects).filter(function(aSubject){
					return aSubject != null || aSubject != undefined;
				});
				
				return conf.subject.subjects;
				
			});
			
		};
		
		function resolveObjects(objects) {
			
			var promises = [];
			
			_(objects.objects).each(function(objectId) {
				promises.push(tenantService.data.object.get({ project_uuid: conf.intraExtension.tenant_uuid, object_uuid: objectId }).$promise);
			});
			
			return $q.all(promises).then(function(data) {
				
				conf.object.objects = _(data).map(function(anObject){
					return _.first(anObject.objects);
				});
				
				conf.object.objects = _(conf.object.objects).filter(function(anObject){
					return anObject != null || anObject != undefined;
				});
				
				return conf.object.objects;
				
			});
			
		};
		
		/*
		 * 
		 */

		function showSubjectAddModal() {
			conf.subject.add.modal.$scope.intraExtension = conf.intraExtension;
			conf.subject.add.modal.$promise.then(conf.subject.add.modal.show);
		};
		
		function showSubjectDeleteModal() {
			conf.subject.del.modal.$scope.subject = conf.selectedSubject;
			conf.subject.del.modal.$promise.then(conf.subject.del.modal.show);
		};
		
		function intraExtensionSubjectCreatedSuccess(event, subject) {
			
			conf.subject.subjects.push(subject);
			conf.subject.selectedSubjects.push(subject);
			
			conf.subject.add.modal.hide();
						
		};
		
		function intraExtensionSubjectCreatedError(event, subject) {
			conf.subject.add.modal.hide();			
		};
		
		/*
		 * 
		 */
		
		function showObjectAddModal() {
			
			
		};
		
		function showObjectDeleteModal() {
			
			
		};
		
	};
	
})();