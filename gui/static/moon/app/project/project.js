/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

angular.module('moonApp.project', ['ngTable', 'ngAnimate', 'mgcrea.ngStrap'])

	.config(function($stateProvider) {
		 
		$stateProvider
	        
		.state('moon.project', {
			url: '/project',
			controller: 'ProjectController',
            templateUrl: 'static/moon/app/project/project.tpl.html'
		});
		 
	})
	 
	.controller('ProjectController', ['$scope', '$filter', '$modal', '$translate', 'ngTableParams', 'alertService', 'projectService', 
	                                   function ($scope, $filter, $modal, $translate, ngTableParams, alertService, projectService) {

		$scope.projectsLoading = true;
		$scope.projects = [];
		 
		/*
		 * list
		 */
		 
		var getData = function() {
			 return $scope.projects;
		};  	
    	
		$scope.projectsTable = new ngTableParams({
	    
			page: 1,            // show first page
			count: 10,          // count per page
			sorting: {
				name: 'asc' // initial sorting
			}
    	
		}, {
	    	
			total: function () { return getData().length; }, // length of data
			getData: function($defer, params) {
	        	
				var orderedData = params.sorting() ?
						
						$filter('orderBy')(getData(), params.orderBy()) : getData();
						$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
	        	
			},
			$scope: { $data: {} }
	        
		});
    	
		projectService.project.query({}, function(data) {
        	
			$scope.projectsLoading = false;
			$scope.projects = data.projects;
        	
			$scope.projectsTable.total($scope.projects.length);
			$scope.projectsTable.reload();
        	
		});
		 
		/*
		 * search
		 */
		 
		$scope.query = '';
	    	
		$scope.search = function (project){
		    
			if (project.name.indexOf($scope.query)!=-1 
					|| project.domain.indexOf($scope.query)!=-1) {
				
		        return true;
		    
			}
		    
			return false;
		        
		};
		
		$scope.reset = function() {
			$scope.query = '';
		};
                		 
	}])
	 
	.factory('projectService', function($resource) { 
                                   	
		return {
                 	   	
			project: $resource('./pip/projects/:project_uuid', {}, {
     	   		query: { method: 'GET', isArray: false },
     	   		get: { method: 'GET', isArray: false }
    	   	}),
    	   	
    	   	user: $resource('./pip/projects/:project_uuid/users/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	object: $resource('./pip/projects/:project_uuid/objects/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	role: $resource('./pip/projects/:project_uuid/roles/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	group: $resource('./pip/projects/:project_uuid/groups/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	roleAssigment: $resource('./pip/projects/:project_uuid/assigments/roles/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	}),
    	   	
    	   	groupAssigment: $resource('./pip/projects/:project_uuid/assigments/groups/:user_uuid', {}, {
    	   		query: { method: 'GET', isArray: true },
     	   		get: { method: 'GET', isArray: false }    	   		
    	   	})
        
        };
    
    })
	 	 
;