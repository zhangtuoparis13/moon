/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.intraExtension', ['ngTable', 'ngAnimate', 'mgcrea.ngStrap'])

	 .config(function($stateProvider) {
		 
		 $stateProvider
	        
     	.state('moon.intraExtension', {
             url: '/intraExtension',
             controller: 'IntraExtensionController',
             templateUrl: 'static/moon/app/intra-extension/intra-extension.tpl.html'
         });
		 
	 })
	 
	 .controller('IntraExtensionController', ['$scope', function ($scope) {

		 // TODO
		 
	 }])
	 
;