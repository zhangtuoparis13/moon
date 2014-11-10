/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionRuleController', IntraExtensionRuleController);
	
	IntraExtensionRuleController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService', 'subjectCategories', 'subjectCategoryValues', 'objectCategories', 'objectCategoryValues', 'rules'];
	
	function IntraExtensionRuleController($scope, $translate, alertService, intraExtensionService, subjectCategories, subjectCategoryValues, objectCategories, objectCategoryValues, rules) {
		
		var rule = this;
		
		/*
		 * 
		 */
		
		rule.subjectCategory = { loading: true, list: [], selected: null };
		rule.subjectCategoryValue = { selected: null, setCurrent: setCurrentSubjectCategoryValue, reset: resetSubjectCategoryValue, hasValue: hasSubjectCategoryValue };
		
		rule.objectCategory = { loading: true, list: [], selected: null };
		rule.objectCategoryValue = { selected: null, setCurrent: setCurrentObjectCategoryValue, reset: resetObjectCategoryValue, hasValue: hasObjectCategoryValue };
		
		rule.rules = { loading: true, list: [] };
		
		/*
		 * 
		 */
		
		resolveRules(rules);
		
		resolveSubjectCategoriesAndValues(subjectCategories, subjectCategoryValues);
		resolveObjectCategoriesAndValues(objectCategories, objectCategoryValues);
		
		/*
		 * 
		 */
		
		function resolveRules(rules) {
		
			// --- rule definition
			// { subject: { categories: [{name: '', values: ''}] }, object: { categories: [{name: '', values: ''}] } }
			
			rule.rules.list = intraExtensionService.transform.rule.getRulesFromRaw(rules);
			rule.rules.loading = false;
			
			return rule.rules.list;
			
		};
		
		function resolveSubjectCategoriesAndValues(subjectCategories, subjectCategoryValues) {
			
			rule.subjectCategory.list = intraExtensionService.transform.category.getCategoriesFromRaw(subjectCategories.subject_categories, subjectCategoryValues.subject_category_values);
			rule.subjectCategory.loading = false;
			
			return rule.subjectCategory.list; 
			
		};
		
		function resolveObjectCategoriesAndValues(objectCategories, objectCategoryValues) {
			
			rule.objectCategory.list = intraExtensionService.transform.category.getCategoriesFromRaw(objectCategories.object_categories, objectCategoryValues.object_category_values);
			rule.objectCategory.loading = false;
			
			return rule.objectCategory.list; 
			
		};
		
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
		
		
	};
	
})();