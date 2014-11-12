/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionAddRuleController', IntraExtensionAddRuleController);
	
	IntraExtensionAddRuleController.$inject = ['$scope', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionAddRuleController($scope, $translate, alertService, intraExtensionService) {
		
		var add = this;
		
		/*
		 * 
		 */
		
		add.intraExtension = $scope.intraExtension;
		
		add.subjectCategory = $scope.subjectCategory;
		add.subjectCategoryValue = { selected: null, reset: resetSubjectCategoryValue };
		add.addSubjectRelation = addSubjectRelation;
		add.canAddSubjectRelation = canAddSubjectRelation;
		add.deleteSubjectRelation = deleteSubjectRelation;
		add.hasSubjectRelations = hasSubjectRelations; 
		
		add.objectCategory = $scope.objectCategory;
		add.objectCategoryValue = { selected: null, reset: resetObjectCategoryValue };
		add.addObjectRelation = addObjectRelation;
		add.canAddObjectRelation = canAddObjectRelation;
		add.deleteObjectRelation = deleteObjectRelation;
		add.hasObjectRelations = hasObjectRelations;
		
		add.hasRelation = hasRelation;
		
		add.rule = { subjects: { categories: [] }, objects: { categories: [] } };
		
		add.canCreateRule = canCreateRule;
		add.create = createRelation;
		
		/*
		 * 
		 */
		
		function hasRelation(relations, category) {
			
			return _(relations).find(function(aRelation) {
				return aRelation.name === category;
			});
			
		};
		
		/*
		 * subject
		 */
			
		function resetSubjectCategoryValue() {
			add.subjectCategoryValue.selected = null;
		};
		
		function addSubjectRelation() {
			
			var catName = add.subjectCategory.selected.name;
			var catValue = add.subjectCategoryValue.selected;
			
			if(!add.hasRelation(add.rule.subjects.categories, catName, catValue)) {
				add.rule.subjects.categories.push({name: catName, value: catValue});
			}
			
			return add.rule.subjects.categories;
			
		};
		
		function canAddSubjectRelation() {
			return add.subjectCategory.selected && add.subjectCategoryValue.selected;			
		};
		
		function deleteSubjectRelation(relation) {
			
			add.rule.subjects.categories = _(add.rule.subjects.categories).reject(function(aRelation) {
				return aRelation.name === relation.name;
			});
			
			return add.rule.subjects.categories;
			
		};
		
		function hasSubjectRelations() {
			return add.rule.subjects.categories.length > 0;
		}
		
		/*
		 * object
		 */
		
		function resetObjectCategoryValue() {
			add.objectCategoryValue.selected = null;
		};
				
		function addObjectRelation() {
			
			var catName = add.objectCategory.selected.name;
			var catValue = add.objectCategoryValue.selected;
			
			if(!add.hasRelation(add.rule.objects.categories, catName, catValue)) {	
				add.rule.objects.categories.push({name: catName, value: catValue});
			}
			
			return add.rule.objects.categories;
			
		};
		
		function canAddObjectRelation() {
			return add.objectCategory.selected && add.objectCategoryValue.selected;			
		};
		
		function deleteObjectRelation(relation) {
			
			add.rule.objects.categories = _(add.rule.objects.categories).reject(function(aRelation) {
				return aRelation.name === relation.name;
			});
			
			return add.rule.objects.categories;
			
		};
		
		function hasObjectRelations() {
			return add.rule.objects.categories.length > 0;
		};
		
		/*
		 * 
		 */
		
		function canCreateRule() {
			return add.hasSubjectRelations() && add.hasObjectRelations();			
		};
		
		function createRelation() {
			
			var rule = { sub_cat_value: { relation_super: {} }, obj_cat_value: { relation_super: {} } };
			
			_(add.rule.subjects.categories).each(function(aRelation) {
				rule.sub_cat_value.relation_super[aRelation.name] = aRelation.value;
			});
			
			_(add.rule.objects.categories).each(function(aRelation) {
				rule.obj_cat_value.relation_super[aRelation.name] = aRelation.value;
			});
			
			intraExtensionService.data.rule.create({ie_uuid: add.intraExtension._id}, rule, createSuccess, createError);
			
			function createSuccess(data) {
				
				$translate('moon.intraExtension.rule.add.success').then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:ruleCreatedSuccess', add.rule);
				
			};
			
			function createError(reason) {
				
				$translate('moon.intraExtension.rule.add.error').then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
				
				$scope.$emit('event:ruleCreatedError', add.rule);
				
			};
			
		};
		
	};
	
})();