/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionConfigurationController', IntraExtensionConfigurationController);
	
	IntraExtensionConfigurationController.$inject = ['$q', 
	                                                 '$rootScope', 
	                                                 '$scope', 
	                                                 '$translate', 
	                                                 '$modal', 
	                                                 'alertService', 
	                                                 'tenantService', 
	                                                 'intraExtensionService', 
	                                                 'intraExtension', 
	                                                 'tenant', 
	                                                 'subjects', 
	                                                 'subjectCategories', 
	                                                 'subjectCategoryValues', 
	                                                 'subjectAssignments', 
	                                                 'objects', 
	                                                 'objectCategories', 
	                                                 'objectCategoryValues', 
	                                                 'objectAssignments'];
	
	function IntraExtensionConfigurationController($q, 
												   $rootScope, 
												   $scope, 
												   $translate, 
												   $modal, 
												   alertService, 
												   tenantService, 
												   intraExtensionService, 
												   intraExtension, 
												   tenant, 
												   subjects, 
												   subjectCategories, 
												   subjectCategoryValues, 
												   subjectAssignments, 
												   objects, 
												   objectCategories, 
												   objectCategoryValues, 
												   objectAssignments) {
		
		var conf = this;
		
		/*
		 * 
		 */
		
		conf.intraExtension = intraExtension.intra_extensions;
		conf.intraExtension.tenant = _.first(tenant.projects);
		
		conf.subject = { loading: true, list: [], selected: null };
		conf.subjectCategory = { loading: true, list: [], selected: null };
		conf.subjectCategoryValue = { selected: null, reset: resetSubjectCategoryValue };
		conf.subjectAssignment = { loading: true, list: [] };
		
		conf.object = { loading: true, list: [], selected: null };
		conf.objectCategory = { loading: true, list: [], selected: null };
		conf.objectCategoryValue = { selected: null, reset: resetObjectCategoryValue };
		conf.objectAssignment = { loading: true, list: [] };
		
		conf.action = {
				subject: {
					add: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-add.tpl.html', show: false }), 
					 	showModal: showSubjectAddModal
					},
					del: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-delete.tpl.html', show: false }), 
					 	showModal: showSubjectDeleteModal
					}
				},
				subjectCategory: {
					add: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-category-add.tpl.html', show: false }), 
					 	showModal: showSubjectCategoryAddModal
					},
					del: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-category-delete.tpl.html', show: false }), 
					 	showModal: showSubjectCategoryDeleteModal
					}
				},
				subjectCategoryValue: {
					add: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-category-value-add.tpl.html', show: false }), 
					 	showModal: showSubjectCategoryValueAddModal
					},
					del: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-category-value-delete.tpl.html', show: false }), 
					 	showModal: showSubjectCategoryValueDeleteModal
					}
				},
				subjectAssignment: {
					add: {
						
					},
					del: {
						
					}
				},
				object: {
					add: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-add.tpl.html', show: false }), 
					 	showModal: showObjectAddModal
					},
					del: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-delete.tpl.html', show: false }), 
					 	showModal: showObjectDeleteModal
					}
				},
				objectCategory: {
					add: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-category-add.tpl.html', show: false }), 
					 	showModal: showObjectCategoryAddModal
					},
					del: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-category-delete.tpl.html', show: false }), 
					 	showModal: showObjectCategoryDeleteModal
					}
				},
				objectCategoryValue: {
					add: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-category-value-add.tpl.html', show: false }), 
					 	showModal: showObjectCategoryValueAddModal
					},
					del: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-category-value-delete.tpl.html', show: false }), 
					 	showModal: showObjectCategoryValueDeleteModal
					}
				},
				objectAssignment: {
					add: {
						
					},
					del: {
						
					}
				}
		};
		
		resolveSubjects(subjects);
		resolveObjects(objects);
		
		resolveSubjectCategoriesAndValues(subjectCategories, subjectCategoryValues);
		resolveObjectCategoriesAndValues(objectCategories, objectCategoryValues);
		
		/*
		 * events
		 */
		
		var rootListeners = {
				
				'event:intraExtensionSubjectCreatedSuccess': $rootScope.$on('event:intraExtensionSubjectCreatedSuccess', intraExtensionSubjectCreatedSuccess),
				'event:intraExtensionSubjectCreatedError': $rootScope.$on('event:intraExtensionSubjectCreatedError', intraExtensionSubjectCreatedError),
				
				'event:intraExtensionSubjectCategoryCreatedSuccess': $rootScope.$on('event:intraExtensionSubjectCategoryCreatedSuccess', intraExtensionSubjectCategoryCreatedSuccess),
				'event:intraExtensionSubjectCategoryCreatedError': $rootScope.$on('event:intraExtensionSubjectCategoryCreatedError', intraExtensionSubjectCategoryCreatedError),
				
				'event:intraExtensionSubjectCategoryValueCreatedSuccess': $rootScope.$on('event:intraExtensionSubjectCategoryValueCreatedSuccess', intraExtensionSubjectCategoryValueCreatedSuccess),
				'event:intraExtensionSubjectCategoryValueCreatedError': $rootScope.$on('event:intraExtensionSubjectCategoryValueCreatedError', intraExtensionSubjectCategoryValueCreatedError),
								
				'event:intraExtensionSubjectDeletedSuccess': $rootScope.$on('event:intraExtensionSubjectDeletedSuccess', intraExtensionSubjectDeletedSuccess),
				'event:intraExtensionSubjectDeletedError': $rootScope.$on('event:intraExtensionSubjectDeletedError', intraExtensionSubjectDeletedError),
				
				'event:intraExtensionSubjectCategoryDeletedSuccess': $rootScope.$on('event:intraExtensionSubjectCategoryDeletedSuccess', intraExtensionSubjectCategoryDeletedSuccess),
				'event:intraExtensionSubjectCategoryDeletedError': $rootScope.$on('event:intraExtensionSubjectCategoryDeletedError', intraExtensionSubjectCategoryDeletedError),
				
				'event:intraExtensionSubjectCategoryValueDeletedSuccess': $rootScope.$on('event:intraExtensionSubjectCategoryValueDeletedSuccess', intraExtensionSubjectCategoryValueDeletedSuccess),
				'event:intraExtensionSubjectCategoryValueDeletedError': $rootScope.$on('event:intraExtensionSubjectCategoryValueDeletedError', intraExtensionSubjectCategoryValueDeletedError),
				
				'event:intraExtensionObjectCreatedSuccess': $rootScope.$on('event:intraExtensionObjectCreatedSuccess', intraExtensionObjectCreatedSuccess),
				'event:intraExtensionObjectCreatedError': $rootScope.$on('event:intraExtensionObjectCreatedError', intraExtensionObjectCreatedError),
				
				'event:intraExtensionObjectCategoryCreatedSuccess': $rootScope.$on('event:intraExtensionObjectCategoryCreatedSuccess', intraExtensionObjectCategoryCreatedSuccess),
				'event:intraExtensionObjectCategoryCreatedError': $rootScope.$on('event:intraExtensionObjectCategoryCreatedError', intraExtensionObjectCategoryCreatedError),
				
				'event:intraExtensionObjectCategoryValueCreatedSuccess': $rootScope.$on('event:intraExtensionObjectCategoryValueCreatedSuccess', intraExtensionObjectCategoryValueCreatedSuccess),
				'event:intraExtensionObjectCategoryValueCreatedError': $rootScope.$on('event:intraExtensionObjectCategoryValueCreatedError', intraExtensionObjectCategoryValueCreatedError),
								
				'event:intraExtensionObjectDeletedSuccess': $rootScope.$on('event:intraExtensionObjectDeletedSuccess', intraExtensionObjectDeletedSuccess),
				'event:intraExtensionObjectDeletedError': $rootScope.$on('event:intraExtensionObjectDeletedError', intraExtensionObjectDeletedError),
				
				'event:intraExtensionObjectCategoryDeletedSuccess': $rootScope.$on('event:intraExtensionObjectCategoryDeletedSuccess', intraExtensionObjectCategoryDeletedSuccess),
				'event:intraExtensionObjectCategoryDeletedError': $rootScope.$on('event:intraExtensionObjectCategoryDeletedError', intraExtensionObjectCategoryDeletedError),
				
				'event:intraExtensionObjectCategoryValueDeletedSuccess': $rootScope.$on('event:intraExtensionObjectCategoryValueDeletedSuccess', intraExtensionObjectCategoryValueDeletedSuccess),
				'event:intraExtensionObjectCategoryValueDeletedError': $rootScope.$on('event:intraExtensionObjectCategoryValueDeletedError', intraExtensionObjectCategoryValueDeletedError),
				
		};
		
		for (var unbind in rootListeners) {
			  $scope.$on('$destroy', rootListeners[unbind]);
		}
		
		/*
		 * resolve
		 */
		
		function resolveSubjects(subjects) {
			
			var promises = [];
			
			_(subjects.subjects).each(function(subjectId) {
				promises.push(tenantService.data.subject.get({ project_uuid: conf.intraExtension.tenant_uuid, user_uuid: subjectId }).$promise);
			});
			
			return $q.all(promises).then(function(data) {
				
				conf.subject.list = _(data).map(function(aSubject){
					return _.first(aSubject.users);
				});
				
				conf.subject.list = _(conf.subject.list).filter(function(aSubject){
					return aSubject != null || aSubject != undefined;
				});
				
				conf.subject.loading = false;
				
				return conf.subject.list;
				
			});
			
		};
		
		function resolveObjects(objects) {
			
			var promises = [];
			
			_(objects.objects).each(function(objectId) {
				promises.push(tenantService.data.object.get({ project_uuid: conf.intraExtension.tenant_uuid, object_uuid: objectId }).$promise);
			});
			
			return $q.all(promises).then(function(data) {
				
				conf.object.list = _(data).map(function(anObject){
					return _.first(anObject.objects);
				});
				
				conf.object.list = _(conf.object.list).filter(function(anObject){
					return anObject != null || anObject != undefined;
				});
				
				conf.object.loading = false;
				
				return conf.object.list;
				
			});
			
		};
		
		function resolveSubjectCategoriesAndValues(subjectCategories, subjectCategoryValues) {
			
			conf.subjectCategory.list = _(subjectCategories.subject_categories).map(function(aCategory) {
				
				return { name: aCategory, 
						 values: subjectCategoryValues.subject_category_values[aCategory] };
				
			});
			
			conf.subjectCategory.loading = false;
			
			return conf.subjectCategory.list; 
			
		};
		
		function resolveObjectCategoriesAndValues(objectCategories, objectCategoryValues) {
			
			conf.objectCategory.list = _(objectCategories.object_categories).map(function(aCategory) {
				
				return { name: aCategory, 
						 values: objectCategoryValues.object_category_values[aCategory] };
				
			});
			
			conf.objectCategory.loading = false;
			
			return conf.objectCategory.list; 
			
		};
		
		/*
		 * add subject
		 */

		function showSubjectAddModal() {
			
			conf.action.subject.add.modal.$scope.intraExtension = conf.intraExtension;
			
			conf.action.subject.add.modal.$promise.then(conf.action.subject.add.modal.show);
			
		};
				
		function intraExtensionSubjectCreatedSuccess(event, subject) {
			
			conf.subject.list.push(subject);
			conf.subject.selected = subject;
			
			conf.action.subject.add.modal.hide();
						
		};
		
		function intraExtensionSubjectCreatedError(event, subject) {
			conf.action.subject.add.modal.hide();			
		};
		
		/*
		 * delete subject
		 */
				
		function showSubjectDeleteModal() {
			
			if(conf.subject.selected) {
			
				conf.action.subject.del.modal.$scope.intraExtension = conf.intraExtension;
				conf.action.subject.del.modal.$scope.subject = conf.subject.selected;
				
				conf.action.subject.del.modal.$promise.then(conf.action.subject.del.modal.show);
			
			}
			
		};
		
		function intraExtensionSubjectDeletedSuccess(event, subject) {
			
			conf.subject.list = _.chain(conf.subject.list).reject({uuid: subject.uuid}).value();
			conf.subject.selected = null;
			
			conf.action.subject.del.modal.hide();
			
		};
		
		function intraExtensionSubjectDeletedError(event, subject) {
			
			conf.action.subject.del.modal.hide();
			
		};
		
		/*
		 * add subject category
		 */
		
		function resetSubjectCategoryValue() {
			conf.subjectCategoryValue.selected = null;
		};

		function showSubjectCategoryAddModal() {

			conf.action.subjectCategory.add.modal.$scope.intraExtension = conf.intraExtension;
			conf.action.subjectCategory.add.modal.$promise.then(conf.action.subjectCategory.add.modal.show);
			
		};
		
		function intraExtensionSubjectCategoryCreatedSuccess(event, category) {
			
			conf.subjectCategory.list.push(category);
			conf.subjectCategory.selected = category;
			
			conf.action.subjectCategory.add.modal.hide();	
			
		};
		
		function intraExtensionSubjectCategoryCreatedError(event, category) {
			conf.action.subjectCategory.add.modal.hide();				
		};
		
		/*
		 * delete subject category
		 */
		
		function showSubjectCategoryDeleteModal() {
			
			if(conf.subjectCategory.selected) {
				
				conf.action.subjectCategory.del.modal.$scope.intraExtension = conf.intraExtension;
				conf.action.subjectCategory.del.modal.$scope.category = conf.subjectCategory.selected;
				
				conf.action.subjectCategory.del.modal.$promise.then(conf.action.subjectCategory.del.modal.show);
			
			}
			
		};
		
		function intraExtensionSubjectCategoryDeletedSuccess(event, category) {
			
			conf.subjectCategory.list = _.chain(conf.subjectCategory.list).reject({name: category.name}).value();
			conf.subjectCategory.selected = null;
			
			conf.action.subjectCategory.del.modal.hide();
			
		};
		
		function intraExtensionSubjectCategoryDeletedError(event, category) {
			
			conf.action.subjectCategory.del.modal.hide();
			
		};
		
		/*
		 * add subject category value
		 */
		
		function showSubjectCategoryValueAddModal() {
			
			if(conf.subjectCategory.selected) {
				
				conf.action.subjectCategoryValue.add.modal.$scope.intraExtension = conf.intraExtension;
				conf.action.subjectCategoryValue.add.modal.$scope.category = conf.subjectCategory.selected;
				
				conf.action.subjectCategoryValue.add.modal.$promise.then(conf.action.subjectCategoryValue.add.modal.show);
				
			}			
			
		};
		
		function intraExtensionSubjectCategoryValueCreatedSuccess(event, categoryAndValue) {
			
			var category = _(conf.subjectCategory.list).find(function(aCategory) {
				return aCategory.name === categoryAndValue.category.name; 
			});	
			
			category.values.push(categoryAndValue.value);
			
			conf.subjectCategoryValue.selected = categoryAndValue.value;
			
			conf.action.subjectCategoryValue.add.modal.hide();
			
		};
		
		function intraExtensionSubjectCategoryValueCreatedError(event, categoryAndValue) {
			
			conf.action.subjectCategoryValue.add.modal.hide();
			
		};
		
		/*
		 * delete subject category value
		 */
		
		function showSubjectCategoryValueDeleteModal() {
			
			if(conf.subjectCategoryValue.selected) {
				
				conf.action.subjectCategoryValue.del.modal.$scope.intraExtension = conf.intraExtension;
				conf.action.subjectCategoryValue.del.modal.$scope.category = conf.subjectCategory.selected;
				conf.action.subjectCategoryValue.del.modal.$scope.value = conf.subjectCategoryValue.selected;
				
				conf.action.subjectCategoryValue.del.modal.$promise.then(conf.action.subjectCategoryValue.del.modal.show);
				
			}
			
		};
		
		function intraExtensionSubjectCategoryValueDeletedSuccess(event, categoryAndValue) {
			
			var category = _(conf.subjectCategory.list).find(function(aCategory) {
				return aCategory.name === categoryAndValue.category.name; 
			});	
			
			category.values = _.chain(category.values).without(categoryAndValue.value).value();
			
			conf.subjectCategoryValue.selected = null;
			
			conf.action.subjectCategoryValue.del.modal.hide();
			
		};
		
		function intraExtensionSubjectCategoryValueDeletedError(event, categoryAndValue) {
			
			conf.action.subjectCategoryValue.del.modal.hide();
			
		};
		
		/*
		 * add object
		 */
				
		function showObjectAddModal() {
			
			conf.action.object.add.modal.$scope.intraExtension = conf.intraExtension;
			
			conf.action.object.add.modal.$promise.then(conf.action.object.add.modal.show);	
			
		};
				
		function intraExtensionObjectCreatedSuccess(event, object) {
			
			conf.object.list.push(object);
			conf.object.selected = object;
			
			conf.action.object.add.modal.hide();
			
		};
		
		function intraExtensionObjectCreatedError() {
			
			conf.action.object.add.modal.hide();
			
		};
		
		/*
		 * delete object
		 */
				
		function showObjectDeleteModal() {
			
			if(conf.object.selected) {
			
				conf.object.action.del.modal.$scope.intraExtension = conf.intraExtension;
				conf.object.action.del.modal.$scope.object = conf.object.current;
				
				conf.object.action.del.modal.$promise.then(conf.object.action.del.modal.show);
			
			}
			
		};
		
		function intraExtensionObjectDeletedSuccess(event, object) {
			
			conf.object.list = _.chain(conf.object.list).reject({uuid: object.uuid}).value();
			conf.object.selected = null;
			
			conf.object.action.del.modal.hide();
			
		};
		
		function intraExtensionObjectDeletedError(event, object) {
			
			conf.object.action.del.modal.hide();
			
		};
		
		/*
		 * add object category
		 */
		
		function resetObjectCategoryValue() {
			conf.objectCategoryValue.selected = null;
		};

		function showObjectCategoryAddModal() {
			
			conf.action.objectCategory.add.modal.$scope.intraExtension = conf.intraExtension;
			conf.action.objectCategory.add.modal.$promise.then(conf.action.objectCategory.add.modal.show);
			
		};
		
		function intraExtensionObjectCategoryCreatedSuccess(event, category) {
			
			conf.objectCategory.list.push(category);
			conf.objectCategory.selected = category;
			
			conf.action.objectCategory.add.modal.hide();	
			
		};
		
		function intraExtensionObjectCategoryCreatedError(event, category) {
			
			conf.action.objectCategory.add.modal.hide();
			
		};
		
		/*
		 * delete object category
		 */
		
		function showObjectCategoryDeleteModal() {
			
			if(conf.objectCategory.selected) {
				
				conf.action.objectCategory.del.modal.$scope.intraExtension = conf.intraExtension;
				conf.action.objectCategory.del.modal.$scope.category = conf.objectCategory.selected;
				
				conf.action.objectCategory.del.modal.$promise.then(conf.action.objectCategory.del.modal.show);
			
			}
			
		};
		
		function intraExtensionObjectCategoryDeletedSuccess(event, category) {
			
			conf.objectCategory.list = _.chain(conf.objectCategory.list).reject({name: category.name}).value();
			conf.objectCategory.selected = null;
			
			conf.action.objectCategory.del.modal.hide();
			
		};
		
		function intraExtensionObjectCategoryDeletedError(event, category) {
			
			conf.action.objectCategory.del.modal.hide();
			
		};
		
		/*
		 * add object category value
		 */
		
		function showObjectCategoryValueAddModal() {
			
			
		};
		
		function intraExtensionObjectCategoryValueCreatedSuccess(event, objectAndValue) {
			
			
		};
		
		function intraExtensionObjectCategoryValueCreatedError(event, objectAndValue) {
			
			
		};
		
		/*
		 * delete object category value
		 */
		
		function showObjectCategoryValueDeleteModal() {
			
			
		};
		
		function intraExtensionObjectCategoryValueDeletedSuccess(event, objectAndValue) {
			
			
		};
		
		function intraExtensionObjectCategoryValueDeletedError(event, objectAndValue) {
			
			
		};
		
	};
	
})();