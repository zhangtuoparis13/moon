/**
 * @author arnaud marhin<arnaud.marhin@orange.com>
 */

(function() {

	'use strict';
					
	angular
		.module('moon')
			.controller('InterExtensionListController', InterExtensionListController);
	
	function InterExtensionListController() {

    var list = this;



		//for (var unbind in rootListeners) {
		//	  $scope.$on('$destroy', rootListeners[unbind]);
		//}

		/*
		 *
		 */

		function getExtraExtensions() {
			return (list.extraExtensions) ? list.extraExtensions : [];
		};

		function hasExtraExtensions() {
			return list.getExtraExtensions().length > 0;
		};

		function addExtraExtension(extraExtension) {
			list.extraExtensions.push(extraExtension);
		};

		function deleteExtraExtension(extraExtension) {
			list.extraExtensions = _.chain(list.extraExtensions).reject({_id: extraExtension._id}).value();
		};

		function refreshExtraExtensions() {

			list.table.total(list.extraExtensions.length);
			list.table.reload();

		};

		function updateExtraExtensions(extraExtension) {

			_(list.extraExtensions).each(function(anExtraExtension) {
        		if(anExtraExtension._id === extraExtension._id) {
        			anExtraExtension = _.clone(extraExtension);
        		}
        	});

			return list.extraExtensions;

		};

	};
	
})();