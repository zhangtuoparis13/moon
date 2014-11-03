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
				
		conf.subject = {
				list: [],
				current: null,
				setCurrent: setCurrentSubject,
				selected: [],
				action: {
					add: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-add.tpl.html', show: false }), 
					 	showModal: showSubjectAddModal
					},
					del: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-delete.tpl.html', show: false }), 
					 	showModal: showSubjectDeleteModal
					}
				},
				category: {
					list: [],
					selected: null,
					action: {
						addCategory: {
							modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-category-add.tpl.html', show: false }), 
						 	showModal: showSubjectCategoryAddModal
						},
						delCategory: {
							modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-category-delete.tpl.html', show: false }), 
						 	showModal: showSubjectCategoryDeleteModal
						},
						addCategoryValue: {
							modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-category-value-add.tpl.html', show: false }), 
						 	showModal: showSubjectCategoryValueAddModal
						},
						delCategoryValue: {
							modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-subject-category-value-delete.tpl.html', show: false }), 
						 	showModal: showSubjectCategoryValueDeleteModal
						}
					}
				},
				assigments: {
					action: {
						add: {
							
						},
						del: {
							
						}
					}
				}
		};
		
		conf.object = {
				list: [],
				current: null,
				setCurrent: setCurrentObject,
				selected: [],
				action: {
					add: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-add.tpl.html', show: false }), 
					 	showModal: showObjectAddModal
					},
					del: {
						modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-delete.tpl.html', show: false }), 
					 	showModal: showObjectDeleteModal
					}
				},
				category: {
					list: [],
					selected: null,
					action: {
						addCategory: {
							modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-category-add.tpl.html', show: false }), 
						 	showModal: showObjectCategoryAddModal
						},
						delCategory: {
							modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-category-delete.tpl.html', show: false }), 
						 	showModal: showObjectCategoryDeleteModal
						},
						addCategoryValue: {
							modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-category-value-add.tpl.html', show: false }), 
						 	showModal: showObjectCategoryValueAddModal
						},
						delCategoryValue: {
							modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-configure-object-category-value-delete.tpl.html', show: false }), 
						 	showModal: showObjectCategoryValueDeleteModal
						}
					}
				},
				assigments: {
					action: {
						add: {
							
						},
						del: {
							
						}
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
				
				return conf.object.list;
				
			});
			
		};
		
		function resolveSubjectCategoriesAndValues(subjectCategories, subjectCategoryValues) {
			
			conf.subject.category.list = _(subjectCategories.subject_categories).map(function(aCategory) {
				
				return { name: aCategory, 
						 values: subjectCategoryValues.subject_category_values[aCategory] };
				
			});
			
			return conf.subject.category.list; 
			
		};
		
		function resolveObjectCategoriesAndValues(objectCategories, objectCategoryValues) {
			
			conf.object.category.list = _(objectCategories.object_categories).map(function(aCategory) {
				
				return { name: aCategory, 
						 values: objectCategoryValues.object_category_values[aCategory] };
				
			});
			
			return conf.object.category.list; 
			
		};
		
		/*
		 * add subject
		 */
		
		function setCurrentSubject(subject) {
			conf.subject.current = subject;
		};

		function showSubjectAddModal() {
			conf.subject.action.add.modal.$scope.intraExtension = conf.intraExtension;
			conf.subject.action.add.modal.$promise.then(conf.subject.action.add.modal.show);
		};
				
		function intraExtensionSubjectCreatedSuccess(event, subject) {
			
			conf.subject.list.push(subject);
			conf.subject.selected.push(subject);
			conf.subject.current = subject;
			
			conf.subject.action.add.modal.hide();
						
		};
		
		function intraExtensionSubjectCreatedError(event, subject) {
			conf.subject.action.add.modal.hide();			
		};
		
		/*
		 * delete subject
		 */
		
		function removeSubjectFrom(subject, subjectList) {
			return _.chain(subjectList).reject({uuid: subject.uuid}).value();
		};
		
		function showSubjectDeleteModal() {
			
			if(conf.subject.current) {
			
				conf.subject.action.del.modal.$scope.intraExtension = conf.intraExtension;
				conf.subject.action.del.modal.$scope.subject = conf.subject.current;
				
				conf.subject.action.del.modal.$promise.then(conf.subject.action.del.modal.show);
			
			}
			
		};
		
		function intraExtensionSubjectDeletedSuccess(event, subject) {
			
			conf.subject.list = removeSubjectFrom(subject, conf.subject.list);
			conf.subject.selected = removeSubjectFrom(subject, conf.subject.selected);
			
			conf.subject.action.del.modal.hide();
			
		};
		
		function intraExtensionSubjectDeletedError(event, subject) {
			
			conf.subject.action.del.modal.hide();
			
		};
		
		/*
		 * add subject category
		 */

		function showSubjectCategoryAddModal() {
			
			
		};
		
		function intraExtensionSubjectCategoryCreatedSuccess(event, category) {
			
			
		};
		
		function intraExtensionSubjectCategoryCreatedError(event, category) {
			
			
		};
		
		/*
		 * delete subject category
		 */
		
		function showSubjectCategoryDeleteModal() {
			
			
		};
		
		function intraExtensionSubjectCategoryDeletedSuccess(event, category) {
			
			
		};
		
		function intraExtensionSubjectCategoryDeletedError(event, category) {
			
			
		};
		
		/*
		 * add subject category value
		 */
		
		function showSubjectCategoryValueAddModal() {
			
			
		};
		
		function intraExtensionSubjectCategoryValueCreatedSuccess(event, categoryAndValue) {
			
			
		};
		
		function intraExtensionSubjectCategoryValueCreatedError(event, categoryAndValue) {
			
			
		};
		
		/*
		 * delete subject category value
		 */
		
		function showSubjectCategoryValueDeleteModal() {
			
			
		};
		
		function intraExtensionSubjectCategoryValueDeletedSuccess(event, categoryAndValue) {
			
			
		};
		
		function intraExtensionSubjectCategoryValueDeletedError(event, categoryAndValue) {
			
			
		};
		
		/*
		 * add object
		 */
		
		function setCurrentObject(object) {
			conf.object.current = object;
		};
		
		function showObjectAddModal() {
			conf.object.action.add.modal.$scope.intraExtension = conf.intraExtension;
			conf.object.action.add.modal.$promise.then(conf.object.action.add.modal.show);			
		};
				
		function intraExtensionObjectCreatedSuccess(event, object) {
			
			conf.object.list.push(object);
			conf.object.selected.push(object);
			conf.object.current = object;
			
			conf.object.action.add.modal.hide();
			
		};
		
		function intraExtensionObjectCreatedError() {
			conf.object.action.add.modal.hide();
		};
		
		/*
		 * delete object
		 */
		
		function removeObjectFrom(object, objectList) {
			return _.chain(objectList).reject({uuid: object.uuid}).value();
		};
		
		function showObjectDeleteModal() {
			
			if(conf.object.current) {
			
				conf.object.action.del.modal.$scope.intraExtension = conf.intraExtension;
				conf.object.action.del.modal.$scope.object = conf.object.current;
				
				conf.object.action.del.modal.$promise.then(conf.object.action.del.modal.show);
			
			}
			
		};
		
		function intraExtensionObjectDeletedSuccess(event, object) {
			
			conf.object.list = removeObjectFrom(object, conf.object.list);
			conf.object.selected = removeObjectFrom(subobjectject, conf.object.selected);
			
			conf.object.action.del.modal.hide();
			
		};
		
		function intraExtensionObjectDeletedError(event, object) {
			
			conf.object.action.del.modal.hide();
			
		};
		
		/*
		 * add subject category
		 */

		function showObjectCategoryAddModal() {
			
			
		};
		
		function intraExtensionObjectCategoryCreatedSuccess(event, category) {
			
			
		};
		
		function intraExtensionObjectCategoryCreatedError(event, category) {
			
			
		};
		
		/*
		 * delete subject category
		 */
		
		function showObjectCategoryDeleteModal() {
			
			
		};
		
		function intraExtensionObjectCategoryDeletedSuccess(event, category) {
			
			
		};
		
		function intraExtensionObjectCategoryDeletedError(event, category) {
			
			
		};
		
		/*
		 * add subject category value
		 */
		
		function showObjectCategoryValueAddModal() {
			
			
		};
		
		function intraExtensionObjectCategoryValueCreatedSuccess(event, objectAndValue) {
			
			
		};
		
		function intraExtensionObjectCategoryValueCreatedError(event, objectAndValue) {
			
			
		};
		
		/*
		 * delete subject category value
		 */
		
		function showObjectCategoryValueDeleteModal() {
			
			
		};
		
		function intraExtensionObjectCategoryValueDeletedSuccess(event, objectAndValue) {
			
			
		};
		
		function intraExtensionObjectCategoryValueDeletedError(event, objectAndValue) {
			
			
		};
		
	};
	
})();