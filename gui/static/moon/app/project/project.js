/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.tenant', ['ngTable', 'ngAnimate', 'mgcrea.ngStrap'])

	 .config(function($stateProvider) {
		 
		 $stateProvider
	        
     	.state('moon.tenant', {
             url: '/tenant',
             controller: 'TenantController',
             templateUrl: 'static/moon/app/tenant/tenant.tpl.html'
         });
		 
	 })
	 
	 .controller('TenantController', ['$scope', function ($scope) {

		 // TODO
		 
	 }])
	 	 
;