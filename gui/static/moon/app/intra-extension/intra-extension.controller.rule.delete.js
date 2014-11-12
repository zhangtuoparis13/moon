/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('IntraExtensionDeleteRuleController', IntraExtensionDeleteRuleController);
	
	IntraExtensionDeleteRuleController.$inject = ['$scope', '$http', '$translate', 'alertService', 'intraExtensionService'];
	
	function IntraExtensionDeleteRuleController($scope, $http, $translate, alertService, intraExtensionService) {
		
		var del = this;
		
		/*
		 * 
		 */
		
		del.intraExtension = $scope.intraExtension;
		del.rule = $scope.rule;
		
		del.remove = deleteRule;
		
		/*
		 * 
		 */
		
		function deleteRule() {
			
			var rule = { sub_cat_value: { relation_super: {} }, obj_cat_value: { relation_super: {} } };
			
			_(del.rule.subjects).each(function(aRelation) {
				rule.sub_cat_value.relation_super[aRelation.name] = aRelation.value;
			});
			
			_(del.rule.objects).each(function(aRelation) {
				rule.obj_cat_value.relation_super[aRelation.name] = aRelation.value;
			});
			
			// intraExtensionService.data.rule.remove({ie_uuid: del.intraExtension._id}, rule, deleteSuccess, deleteError);
			
			// FIXME: do not send a body in a DELETE request
			$http({url: './json/intra-extensions/' + del.intraExtension._id + '/rules', method: 'DELETE', data: rule}).then(deleteSuccess, deleteError);
			
			function deleteSuccess(data) {
				
				$translate('moon.intraExtension.rule.delete.success', {ruleJson: del.rule}).then(function (translatedValue) {
        			alertService.alertSuccess(translatedValue);
                });	
    			
    			$scope.$emit('event:ruleDeletedSuccess', del.rule);
				
			};
			
			function deleteError(reason) {
				
				$translate('moon.intraExtension.rule.delete.error', {ruleJson: del.rule}).then(function (translatedValue) {
        			alertService.alertError(translatedValue);
                });	
				
				$scope.$emit('event:ruleDeletedError', del.rule);
				
			};
			
		}
		
	};
	
})();