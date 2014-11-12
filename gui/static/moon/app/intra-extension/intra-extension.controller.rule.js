/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionRuleController', IntraExtensionRuleController);
	
	IntraExtensionRuleController.$inject = ['$rootScope', '$scope', '$modal', '$translate', '$filter', 'ngTableParams', 'alertService', 'intraExtensionService', 'intraExtension', 'subjectCategories', 'subjectCategoryValues', 'objectCategories', 'objectCategoryValues', 'rules'];
	
	function IntraExtensionRuleController($rootScope, $scope, $modal, $translate, $filter, ngTableParams, alertService, intraExtensionService, intraExtension, subjectCategories, subjectCategoryValues, objectCategories, objectCategoryValues, rules) {
		
		var list = this;
		
		/*
		 * 
		 */
		
		list.intraExtension = intraExtension.intra_extensions;
		
		list.loading = true
		list.rules = [];
		list.table = {};
		
		list.hasRules = hasRules;
		list.getRules = getRules;
		list.refreshRules = refreshRules;
		
		list.subjectCategory = { loading: true, list: [] };		
		list.objectCategory = { loading: true, list: [] };
		
		list.add = { modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-rule-add.tpl.html', show: false }), 
				 	 showModal: showAddModal };
		
		list.del = { modal: $modal({ template: 'static/moon/app/intra-extension/intra-extension-rule-delete.tpl.html', show: false }), 
			 	 	 showModal: showDeleteModal };
		
		/*
		 * 
		 */
				
		resolveRules(rules);
		
		resolveSubjectCategoriesAndValues(subjectCategories, subjectCategoryValues);
		resolveObjectCategoriesAndValues(objectCategories, objectCategoryValues);
		
		newRulesTable();
		
		/*
		 * 
		 */
		
		function resolveRules(rules) {
		
			// --- rule definition
			// { subjects: { categories: [{name: '', values: ''}] }, objects: { categories: [{name: '', values: ''}] } }
			
			list.rules = intraExtensionService.transform.rule.getRulesFromRaw(rules);
			list.loading = false;
			
			return list.rules;
			
		};
		
		function resolveSubjectCategoriesAndValues(subjectCategories, subjectCategoryValues) {
			
			list.subjectCategory.list = intraExtensionService.transform.category.getCategoriesFromRaw(subjectCategories.subject_categories, subjectCategoryValues.subject_category_values);
			list.subjectCategory.loading = false;
			
			return list.subjectCategory.list; 
			
		};
		
		function resolveObjectCategoriesAndValues(objectCategories, objectCategoryValues) {
			
			list.objectCategory.list = intraExtensionService.transform.category.getCategoriesFromRaw(objectCategories.object_categories, objectCategoryValues.object_category_values);
			list.objectCategory.loading = false;
			
			return list.objectCategory.list; 
			
		};
		
		function newRulesTable() {
			
			list.table = new ngTableParams({
			    
				page: 1,            // show first page
				count: 10          // count per page
	   	
			}, {
		    	
				total: function () { return list.getRules().length; }, // length of data
				getData: function($defer, params) {
		        	
					var orderedData = params.sorting() ? $filter('orderBy')(list.getRules(), params.orderBy()) : list.getRules();
					$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
		        	
				},
				$scope: { $data: {} }
		        
			});
			
			return list.table;
			
		};
		
		/*
		 * ---- events
		 */
		
		var rootListeners = {
				
				'event:ruleCreatedSuccess': $rootScope.$on('event:ruleCreatedSuccess', ruleCreatedSuccess),
				'event:ruleCreatedError': $rootScope.$on('event:ruleCreatedError', ruleCreatedError),
				
				'event:ruleDeletedSuccess': $rootScope.$on('event:ruleDeletedSuccess', ruleDeletedSuccess),
				'event:ruleDeletedError': $rootScope.$on('event:ruleDeletedError', ruleDeletedError)
				
		};
		
		for (var unbind in rootListeners) {
			  $scope.$on('$destroy', rootListeners[unbind]);
		}
		
		/*
		 * 
		 */
		
		function setCurrentSubjectCategoryValue(value) {
			rule.subjectCategoryValue.current = value;
		};
		
		function setCurrentObjectCategoryValue(value) {
			rule.objectCategoryValue.current = value;
		};
		
		function hasSubjectCategoryValue() {
			return rule.subjectCategoryValue.selected;			
		};
		
		function hasObjectCategoryValue() {
			return rule.objectCategoryValue.selected;			
		};
		
		function resetSubjectCategoryValue() {
			rule.subjectCategoryValue.selected = null;
		};
		
		function resetObjectCategoryValue() {
			rule.objectCategoryValue.selected = null;
		};
		
		function getRules() {
			 return list.rules ? list.rules : [];
		};
		
		function hasRules() {
			return list.getRules().length > 0;
		};
		
		function refreshRules() {
			
			list.table.total(list.rules.length);
			list.table.reload();
			
		};
		
		/*
		 * add
		 */
		
		function showAddModal() {
			
			list.add.modal.$scope.intraExtension = list.intraExtension;
						
			list.add.modal.$scope.subjectCategory = list.subjectCategory;
			list.add.modal.$scope.objectCategory = list.objectCategory;
			
        	list.add.modal.$promise.then(list.add.modal.show);
        	
        };
                
        function ruleCreatedSuccess(event, rule) {
        	
        	rule.id = _.uniqueId('rule_');
        	
        	list.rules.push(rule);
        	list.refreshRules();
			
			list.add.modal.hide();
        	
        };
        
        function ruleCreatedError(event, rule) {
        	list.add.modal.hide();
        };
        
        /*
         * delete
         */
        
        function showDeleteModal(rule) {
        	
        	list.del.modal.$scope.intraExtension = list.intraExtension;
        	list.del.modal.$scope.rule = rule;
        	list.del.modal.$promise.then(list.del.modal.show);
        	
        };
        
        function ruleDeletedSuccess(event, rule) {
        	
        	list.rules = _(list.rules).reject(function(aRule) {
        		return aRule.id === rule.id;
        	});
        	
        	list.refreshRules();
			
			list.del.modal.hide();
        	
        };
        
        function ruleDeletedError(event, rule) {
        	list.del.modal.hide();
        };
		
	};
	
})();