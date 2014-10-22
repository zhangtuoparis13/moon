/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.interExtension', ['ngTable', 'ngAnimate', 'mgcrea.ngStrap'])

	 .config(function($stateProvider) {
		 
		 $stateProvider
		 
		 .state('moon.interExtension', {
	            abstract: true,
	            template: '<div ui-view></div>'
		 })
	        
     	.state('moon.interExtension.list', {
             url: '/interExtension',
             controller: 'InterExtensionController',
             templateUrl: 'static/moon/app/inter-extension/inter-extension.tpl.html'
         });
		 
	 })
	 
	 .controller('InterExtensionController', ['$scope', function ($scope) {

		 // TODO
		 
	 }])
	 
;