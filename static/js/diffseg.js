angular.module('DiffsegApp', ['ui.bootstrap', 'angularFileUpload', 'angular-loading-bar', 'ngSanitize', 'ngCookies'])

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])

.controller('MainCtrl', ['$scope', 'FileUploader', '$http', '$cookies', function($scope, FileUploader, $http, $cookies) {

    var csrftoken = $cookies.get('csrftoken');

    if (!csrftoken) {
        $http.get(Urls.seg());  // get csrf cookies;
        var csrftoken = $cookies.get('csrftoken');
    }

    $scope.source_text = {text: '上海自來水來自海上'};

	$scope.segmentators = {
		LIVAC: true,
		Thulac: true,
        DeepSeg: true,
	};

    $scope.seg = function() {
        $scope.segmentators_selected = Object.keys(_.pick($scope.segmentators, _.identity));
        var data = {
            source_text: $scope.source_text.text,
            segmentators: $scope.segmentators_selected,
        };
        $http.post(Urls.seg(), data)
            .then(function(resp) {
                $scope.segs = resp.data;
            });
    };

    $scope.settings = {};
    $scope.settings.uploader = new FileUploader({
        url: '/uploader/'
    });
    $scope.initUploader = function() {
        $scope.settings.uploader = new FileUploader({
            headers : {
                'X-CSRFTOKEN' : csrftoken
            },
            url: Urls().uploader()
        });
    };

}]);