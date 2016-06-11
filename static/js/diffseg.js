angular.module('DiffsegApp', ['angularFileUpload', 'angular-loading-bar'])

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])

.controller('MainCtrl', ['$scope', 'FileUploader', '$http', function($scope, FileUploader, $http) {

    $scope.source_text = '今天天氣很好';

	$scope.segmentators = {
		LIVAC: true,
		DeepSeg: false,
		Thulac: false,
	};

    $scope.seg = function() {
        var data = {
            source_text: $scope.source_text,
            segmentators: Object.keys(_.pick($scope.segmentators, _.identity)),
        };
        $http.post(Urls.seg(), data)
            .then(function(resp) {
                console.log(resp);
            });
    };


}]);