angular.module('DiffsegApp', ['ui.bootstrap', 'angularFileUpload', 'angular-loading-bar', 'ngSanitize', 'ngCookies'])

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])

.controller('MainCtrl', ['$scope', 'FileUploader', '$http', '$cookies', '$sce', function($scope, FileUploader, $http, $cookies, $sce) {

    var csrftoken = $cookies.get('csrftoken');

    if (!csrftoken) {
        $http.get(Urls.seg());  // get csrf cookies;
        var csrftoken = $cookies.get('csrftoken');
    }

    $scope.source_text = {text: '陳男因光頭特徵太明顯，通過走道相當好認，而他才離開40秒，聽到轟轟聲響，驚覺不對勁，雖急忙返回，但已救不了火。軍方表示，戰情室猶如軍艦的心臟，具有高度機敏資料，涉及國防安全，並未安裝監視系統，連拍照或攜帶智慧型手機皆不得，以免軍情外洩，金江艦亦是如此。'};

	$scope.segmentators = {
		LIVAC: true,
		Thulac: true,
        DeepSeg: false,
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
                con = []
                var pat = RegExp('(<span.*?<\/span>)(?! <span)', 'g');
                var html = '';
                // html += '<span uib-dropdown on-toggle="toggled(open)">';
                // html += '    <a href uib-dropdown-toggle>';
                // html += '        Click me for a dropdown, yo!';
                // html += '    </a>';
                // html += '    <ul class="dropdown-menu" uib-dropdown-menu aria-labelledby="simple-dropdown">';
                // html += '        <li ng-repeat="choice in items">';
                // html += '            <a href>{{choice}}</a>';
                // html += '        </li>';
                // html += '    </ul>';
                // html += '</span>';
                html = '<span class="diffgroup">' + html + '</span>';
                angular.forEach($scope.segs, function(value, key) {
                    var matched_words = value.match(pat);
                    con.push(matched_words);
                });
                con = _.zip(...con);
                con = con.map(function(lst) {
                    return lst.map(function(text) {
                        return text ? String(text).replace(/<[^>]+>/gm, '') : '';
                    })
                })
                $scope.con = con;
                $scope.same = $scope.segs[0].replace(pat, html);
                setTimeout(function() {
                    $('.diffgroup').each(function(idx) {
                        var content = $(this);
                        content.append('<select ng-model="test[' + idx + ']" ng-options="i for i in con[' + idx + ']"></select>');
                        angular.element(document).injector().invoke(function($compile) {
                            var scope = angular.element(content).scope();
                            $compile(content)(scope);
                        });
                    });
                }, 300);
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
