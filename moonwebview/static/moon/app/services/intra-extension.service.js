/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';

	angular
		.module('moon')
				.factory('intraExtensionService', intraExtensionService);
	
	intraExtensionService.$inject = ['$q', '$resource', 'INTRA_EXTENSION_CST','REST_URI'];
	
	function intraExtensionService($q, $resource, INTRA_EXTENSION_CST, REST_URI) {
		
		return {
			
			data: {
			
				intraExtension: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid', {}, {
	     	   		query: { method: 'GET', isArray: false },
	     	   		get: { method: 'GET', isArray: false },
	     	   		create: { method: 'POST' },
	     	   		remove: { method: 'DELETE' }
	    	   	}),
	    	   	    	   	
	    	   	tenant: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/tenant', {}, {
	     	   		query: { method: 'GET', isArray: false }
	    	   	}),
	     	   	
				policy: $resource(REST_URI.INTRAEXTENSION + '/policies', {}, {
	     	   		query: { method: 'GET', isArray: false }
	    	   	}),
	    	   	
	    	   	subject: {
	    	   		
	    	   		subject: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/subjects/:subject_uuid', {}, {
		    	   		query: { method: 'GET', isArray: false },
		     	   		get: { method: 'GET', isArray: false },
		     	   		create: { method: 'POST' },
		     	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	category: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/subject_categories/:category_name', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	categoryValue: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/subject_category_values/:category/:value', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	assignment: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/subject_assignments/:subject_id/:category_id/:value', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	})
	    	   		
	    	   	},
	    	   	
	    	   	object: {
	    	   		
	    	   		object: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/objects/:object_uuid', {}, {
		    	   		query: { method: 'GET', isArray: false },
		     	   		get: { method: 'GET', isArray: false },
		     	   		create: { method: 'POST' },
		     	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	category: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/object_categories/:category_name', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	}),
		    	   	
		    	   	categoryValue: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/object_category_values/:category/:value', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	}),		    	   	
		    	   	
		    	   	assignment: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/object_assignments/:object_id/:category_id/:value', {}, {
		    	   		query: { method: 'GET', isArray: false },
		    	   		create: { method: 'POST' },
		    	   		remove: { method: 'DELETE' }
		    	   	})
	    	   		
	    	   	},
	    	   	
	    	   	rule: $resource(REST_URI.INTRAEXTENSION + '/:ie_uuid/rules', {}, {
	     	   		query: { method: 'GET', isArray: false },
	     	   		create: { method: 'POST' },
	     	   		remove: { method: 'DELETE' }
	    	   	})
    	   	
			},
			
			findAll: function() {

    	   		var _self = this;
    	   		
    	   		return this.data.intraExtension.query().$promise.then(function(result) {

    	   			return _.map(result.intra_extensions, function(uuid) {
    	   				return _self.findOne(uuid);
    	   			}); 

    	   		}).then(function(uuids) {
	   					    	   			
    	   			return $q.all(uuids).then(function(result) {
    	   				
    	   				return _(result).map(function(resource) {
    	   					return resource.intra_extensions;
    	   				});
    	   				    	   				    	   				
    	   			});

	   			});

	   		},
	   		
	   		findOne: function(uuid) {
	   			
	   			return this.data.intraExtension.get({ie_uuid: uuid}).$promise;
	   			
	   		},
	   		
	   		findSome: function(uuids) {
	   			
	   			var _self = this;
	   			
	   			var promises = _(uuids).map(function(uuid) {
	   				return _self.findOne(uuid);
	   			});
	   			
	   			return $q.all(promises).then(function(result) {
	   				
	   				return _(result).map(function(resource) {
	   					return resource.intra_extensions;
	   				});
	   				
	   			});
	   			
	   		},
	   		
	   		hasMLSPolicy: function(intraExtension) {
				return intraExtension.intra_extensions.authz.metadata.model === INTRA_EXTENSION_CST.POLICY.MLS.NAME;
			},
				
			hasRBACPolicy: function(intraExtension) {
				return intraExtension.intra_extensions.authz.metadata.model === INTRA_EXTENSION_CST.POLICY.RBAC.NAME;
			},
	   		
	   		transform: {
	   			
	   			category: {
	   				
	   				getCategoriesFromRaw: function(rawCategories, rawCategoriesValues) {
	   					
	   					var categories = _(rawCategories).map(function(aCategory) {
	   						
	   						var catValues = rawCategoriesValues[aCategory];
	   						
	   						if(!catValues) {
	   							catValues = [];
	   						}
	   						
	   						return { name: aCategory, values: catValues };
	   						
	   					});
	   						   					
	   					return categories; 
	   					
	   				}
	   				
	   			},
	   			
	   			assigment: {
	   				
	   				getUuidsFromRaw: function(rawElementAssignments) {
	   					
	   					var uuids = [];
	   					
	   					var elementsRaw = _.values(rawElementAssignments);
	   					
	   					_(elementsRaw).each(function(aRaw) {
	   						uuids = uuids.concat(_.keys(aRaw));
	   					});
	   					
	   					return _.uniq(uuids);
	   					
	   				},
	   				
	   				getRawElementFromUuid: function(rawElements, uuid) {
	   					
	   					return _(rawElements).find(function(anElement) {
	   						return anElement.uuid === uuid;
	   					});
	   					
	   				},
	   				
	   				getElementsFromRaw: function(rawElementAssignments, rawElements) {
	   					
	   					var _self = this;
	   					var list = [];
	   					
	   					var uuids = this.getUuidsFromRaw(rawElementAssignments);
	   					
	   					_(uuids).each(function(aUuid) {
	   						list.push(_self.getRawElementFromUuid(rawElements, aUuid));
	   					});
	   					
	   					return _.compact(list);
	   					
	   				},
	   				
	   				getCategoriesFromRaw: function(rawElementAssignments, rawElement) {
	   					
	   					var categories = [];
	   					
	   					var categoryNames = _.keys(rawElementAssignments);
	   					
	   					_(categoryNames).each(function(categoryName) {
	   						
	   						var categoryValues = rawElementAssignments[categoryName][rawElement.uuid];
	   						
	   						if(categoryValues) {
	   							categories.push({name: categoryName, values: categoryValues});
	   						}
	   						
	   					});
	   					
	   					return categories;
	   					
	   				}
	   				
	   			},
	   			
	   			rule: {
	   					   				
	   				getMetaRule: function(hasRBACPolicy) {
	   					
	   					var metaRule = INTRA_EXTENSION_CST.POLICY.MLS.META_RULE;
	   					
	   					if(hasRBACPolicy) {
	   						metaRule = INTRA_EXTENSION_CST.POLICY.RBAC.META_RULE;
	   					}
	   					
	   					return metaRule;
	   					
	   				},
	   				
	   				getRulesFromRaw: function(rawRules, hasRBACPolicy) {
	   						   					
	   					var metaRule = this.getMetaRule(hasRBACPolicy);
	   					
	   					var _self = this;
	   					var rules = _(rawRules.rules[metaRule]).map(function(aRawRule) {
	   						
	   						var subject = _self.getCategoriesFromRaw(aRawRule.sub_cat_value[metaRule]);
	   						var object = _self.getCategoriesFromRaw(aRawRule.obj_cat_value[metaRule]);
	   							   						
	   						return {id: _.uniqueId(INTRA_EXTENSION_CST.RULE.ID_PREFIX), subjects: subject, objects: object};
	   						
	   					});
	   					
	   					return rules;
	   					
	   				},
	   				
	   				getCategoriesFromRaw: function(rawElement) {
	   					
	   					var categoriesNames = _.keys(rawElement);
	   					
	   					var categories = _(categoriesNames).map(function(aCategoryName) {
	   						return { name: aCategoryName, value: rawElement[aCategoryName] };
	   					});
	   					
	   					return categories;
	   					
	   				}
	   				
	   			}
	   			
	   		},
	   		
	   		assignment: {
	   			
	   			addAssignment: function(assignments, element, category, value) {
	   				
	   				var currentAssignment = _(assignments).find(function(anAssignment) {
	   					return anAssignment.element.uuid === element.uuid;
	   				});
	   				
	   				if(currentAssignment) {
	   					
	   					var currentCategory = _(currentAssignment.categories).find(function(aCategory) {
	   						return aCategory.name === category.name;
	   					});
	   					
	   					if(currentCategory) {
	   						currentCategory.values.push(value);
	   					}
	   					else {
	   						currentAssignment.categories.push({ name: category.name, values: [value] });
	   					}
	   					
	   				}
	   				else {
	   					assignments.push({ element: element, categories: [{ name: category.name, values: [value] }]});
	   				}
	   				
	   				return assignments;
	   				
	   			},
	   			
	   			removeAssignment: function(assignments, element, category, value) {
	   				
	   				var currentAssignment = _(assignments).find(function(anAssignment) {
	   					return anAssignment.element.uuid === element.uuid;
	   				});
	   				
	   				if(currentAssignment) {
	   					
	   					var currentCategory = _(currentAssignment.categories).find(function(aCategory) {
	   						return aCategory.name === category.name;
	   					});
	   					
	   					if(currentCategory) {
	   						
	   						currentCategory.values = _(currentCategory.values).reject(function(aValue) {
	   							return aValue === value;
	   						})

	   						if(_.size(currentCategory.values) == 0) {
	   							
	   							currentAssignment.categories = _(currentAssignment.categories).reject(function(aCategory) {
	   		   						return aCategory.name === currentCategory.name;
	   		   					});
	   							
	   							if(_.size(currentAssignment.categories) == 0) {
	   								
	   								assignments = _(assignments).reject(function(anAssignment) {
	   									return anAssignment.element.uuid === element.uuid;
	   								});
	   								
	   							}
	   							
	   						}
	   						
	   					}
	   					
	   				}
	   				
	   				return assignments;
	   				
	   			}
	   			
	   		}
    	   	
		};
		
	};
	
})();
