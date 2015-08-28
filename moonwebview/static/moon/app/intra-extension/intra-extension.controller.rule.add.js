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
		add.hasRBACPolicy = $scope.hasRBACPolicy;
		
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
		
		add.rule = { subjects: [], objects: [] };
		
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
			
			if(!add.hasRelation(add.rule.subjects, catName, catValue)) {
				add.rule.subjects.push({name: catName, value: catValue});
			}
			
			return add.rule.subjects;
			
		};
		
		function canAddSubjectRelation() {
			return add.subjectCategory.selected && add.subjectCategoryValue.selected;			
		};
		
		function deleteSubjectRelation(relation) {
			
			add.rule.subjects = _(add.rule.subjects).reject(function(aRelation) {
				return aRelation.name === relation.name;
			});
			
			return add.rule.subjects;
			
		};
		
		function hasSubjectRelations() {
			return add.rule.subjects.length > 0;
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
			
			if(!add.hasRelation(add.rule.objects, catName, catValue)) {	
				add.rule.objects.push({name: catName, value: catValue});
			}
			
			return add.rule.objects;
			
		};
		
		function canAddObjectRelation() {
			return add.objectCategory.selected && add.objectCategoryValue.selected;			
		};
		
		function deleteObjectRelation(relation) {
			
			add.rule.objects = _(add.rule.objects).reject(function(aRelation) {
				return aRelation.name === relation.name;
			});
			
			return add.rule.objects;
			
		};
		
		function hasObjectRelations() {
			return add.rule.objects.length > 0;
		};
		
		/*
		 * 
		 */
		
		function canCreateRule() {
			return add.hasSubjectRelations() && add.hasObjectRelations();			
		};
		
		function createRelation() {
			
			var metaRule = intraExtensionService.transform.rule.getMetaRule(add.hasRBACPolicy);
									
			var rule = { sub_cat_value: {}, obj_cat_value: {} };
			
			rule.sub_cat_value[metaRule] = {};
			rule.obj_cat_value[metaRule] = {};
			
			_(add.rule.subjects).each(function(aRelation) {
				rule.sub_cat_value[metaRule][aRelation.name] = aRelation.value;
			});
			
			_(add.rule.objects).each(function(aRelation) {
				rule.obj_cat_value[metaRule][aRelation.name] = aRelation.value;
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