angular.module('DiffsegApp', ['angularFileUpload', 'angular-loading-bar'])

.controller('MainCtrl', ['$scope', 'FileUploader', '$http', function($scope, FileUploader, $http) {
	$scope.segmentators = {
		LIVAC: true,
		DeepSeg: true,
		Thulac: true,
	};
}]);