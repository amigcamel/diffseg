angular.module('DiffsegApp', ['ui.bootstrap', 'angularFileUpload', 'angular-loading-bar', 'ngSanitize'])

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])

.controller('MainCtrl', ['$scope', 'FileUploader', '$http', function($scope, FileUploader, $http) {

    $http.get(Urls.seg());  // get csrf cookies;

    $scope.source_text = '上海自來水來自海上';

	$scope.segmentators = {
		LIVAC: true,
		Thulac: true,
        // DeepSeg: false,
	};

    $scope.seg = function() {
        $scope.segmentators_selected = Object.keys(_.pick($scope.segmentators, _.identity));
        var data = {
            source_text: $scope.source_text,
            segmentators: $scope.segmentators_selected,
        };
        $http.post(Urls.seg(), data)
            .then(function(resp) {
                $scope.segs = resp.data;
            });
    };


}]);