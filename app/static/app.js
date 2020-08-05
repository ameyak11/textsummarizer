var app = angular.module('vartaApp', ['ngMaterial', 'ngAnimate']);

var url_prefix = 'http://127.0.0.1:5000/web/v1/';
var current_id = '';

app.controller('sampleController', ['$scope', function ($scope) {
    $scope.name = 'Suraj';
}]);

app.controller('formController', ['$scope', '$http', '$sce', function ($scope, $http, $sce) {

    $scope.article = {
        title: '',
        content: ''
    };
    $scope.count = "";


    $scope.showCard = true;
    $scope.resp = '';
    var html_code = "<p>";
    $scope.summarizeClicked = function () {
        $scope.showCard = false;
        $scope.showSummaryCard = true;
        $scope.showCommentCard = true;
        $scope.showCard1 = true;
        // console.log(document.getElementById('article_title').value);
        var title = document.getElementById('article_title').value;
        var body = document.getElementById('article_body').value;

        var formdata = new FormData();
        formdata.append('article_title', title);
        formdata.append('article_body', body);
        console.log(formdata);

        var http = new XMLHttpRequest();
        var url = url_prefix + 'summarize_article';
        http.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var jsonResponse = JSON.parse(http.responseText);
                console.log(jsonResponse);
                var sentences = jsonResponse['article_body'];
                var summary = "";
                var indices = jsonResponse['summary_indices'];
                current_id = jsonResponse['_id'];
                console.log("current_id" + current_id);
                // console.log(indices);
                // console.log(typeof indices[0]);
                for (i = 0; i < indices.length; i++) {
                    var j = indices[i];
                    // console.log("j");
                    // console.log(j);
                    summary = summary + sentences[j];
                }
                document.getElementById("card-title").innerHTML = title;
                document.getElementById("card-title1").innerHTML = title;
                document.getElementById("card-contents").innerHTML = summary;
                // document.getElementById("article-contents").innerHTML = body;
                var count = 0;
                for (i = 0; i < sentences.length; i++) {
                    var flag = false;
                    for (j = count; j < indices.length; j++) {
                        if (i === indices[j]) {
                            console.log(i + "and" + indices[j]);
                            html_code += "<mark>" + sentences[i] + "</mark>";
                            flag = true;
                            count++;
                            break;
                        }
                    }
                    if (flag === false) {
                        html_code += sentences[i];
                    }
                }
                html_code += "</p>"
                // console.log(html_code);
                // $scope.customCode = $sce.trustAsHtml(html_code);
                // console.log($scope.customCode);
                document.getElementById("custom-div").innerHTML = html_code;
                $scope.showCommentCard = true;
                console.log("set true");
            }
            else if (this.status != 200) {
                // $scope.showCommentCard = false;
                console.log("set false");
                document.getElementById("card-contents").innerHTML = 'Network error!'
            }
        }
        http.open("POST", url);
        http.send(formdata);
        // scroll
        $('html, body').animate({ scrollTop: 0 }, 'fast');
    };

    $scope.summarizeLinkClicked = function () {
        $scope.showCard = false;
        $scope.showSummaryCard = true;
        $scope.showCommentCard = true;
        $scope.showCard1 = true;

        var article_link = document.getElementById("article_link").value;
        var check = article_link.split(":");
        if (check[0] != "http") {
            article_link = "http://" + article_link;
            console.log(article_link);
        }
        // console.log(article_link);
        // for(i=0;i<4;i++){
        // console.log("prefix"+article_link[i]);
        // }

        var formdata = new FormData();
        formdata.append("article_link", article_link);

        var http = new XMLHttpRequest();
        http.addEventListener("progress", updateProgress);
        // http.addEventListener("load", transferComplete);
        // http.addEventListener("error", transferFailed);
        // http.addEventListener("abort", transferCanceled);

        var url = url_prefix + 'summarize_link';
        http.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var jsonResponse = JSON.parse(http.responseText);
                console.log(jsonResponse);
                var sentences = jsonResponse['article_body'];
                var summary = "";
                var indices = jsonResponse['summary_indices'];
                var title = jsonResponse['article_title'];
                current_id = jsonResponse['_id'];
                console.log("current_id" + current_id);
                // console.log(indices);
                // console.log(typeof indices[0]);
                for (i = 0; i < indices.length; i++) {
                    var j = indices[i];
                    // console.log("j");
                    // console.log(j);
                    summary = summary + sentences[j];
                }
                document.getElementById("card-title").innerHTML = title;
                document.getElementById("card-title1").innerHTML = title;
                document.getElementById("card-contents").innerHTML = summary;
                // document.getElementById("article-contents").innerHTML = body;
                var count = 0;
                for (i = 0; i < sentences.length; i++) {
                    var flag = false;
                    for (j = count; j < indices.length; j++) {
                        if (i === indices[j]) {
                            console.log(i + "and" + indices[j]);
                            html_code += "<mark>" + sentences[i] + "</mark>";
                            flag = true;
                            count++;
                            break;
                        }
                    }
                    if (flag === false) {
                        html_code += sentences[i];
                    }
                }
                html_code += "</p>"
                // console.log(html_code);
                // $scope.customCode = $sce.trustAsHtml(html_code);
                // console.log($scope.customCode);
                document.getElementById("custom-div").innerHTML = html_code;
                $scope.showCommentCard = true;
                console.log("set true");
            }
            else if (this.status != 200) {
                // document.getElementById("card-contents").innerHTML = 'Network error!'
                // console.log("set false");
                document.getElementById("card-contents").innerHTML = 'Loading..'
            }
        }
        http.open("POST", url);
        http.send(formdata);

        function updateProgress(http) {
            if (http.lengthComputable) {
                var percentComplete = http.loaded / http.total;
                console.log("percentComplete:" + percentComplete);
                // ...
            } else {
                // Unable to compute progress information since the total size is unknown
                console.log("cannot compute progress");
            }
        }

    };

    $scope.feedbackClicked = function () {
        // $scope.showCard = false;
        // $scope.showSummaryCard = true;
        // $scope.showCommentCard = false;
        // $scope.showCard1 = true;

        var stars = document.getElementById("input-1").value; //get stars
        console.log("stars:" + stars);
        var is_rated;
        if (stars === "") {
            is_rated = false;
            stars = 0;
        }
        else {
            is_rated = true;
        }
        console.log("is_rated:" + is_rated);
        var comment = "";
        comment = document.getElementById("article_comment").value;
        console.log("comment:" + comment);

        var formdata = new FormData();
        formdata.append('article_id', current_id);
        formdata.append('is_rated', is_rated);
        formdata.append('rating', stars);
        formdata.append('comment', comment);

        console.log(formdata);

        $scope.showCommentCard = false;

        var http = new XMLHttpRequest();
        var url = url_prefix + 'summary_rating';

        http.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var jsonResponse = JSON.parse(http.responseText);
                console.log(jsonResponse);
            }
            else if (this.status != 200) {
                // document.getElementById("card-contents").innerHTML = 'Network error!'

            }
        }
        http.open("POST", url);
        http.send(formdata);
    };

    $scope.customCode = $sce.trustAsHtml(html_code);
    $scope.reloadPage = function () {
        window.location.reload();
        window.scrollTo(0, 0);
    };

}]);

app.controller('StarCtrl', ['$scope', function ($scope) {
    $scope.rating = 0;
    $scope.ratings = [{
        current: 5,
        max: 10
    }, {
        current: 3,
        max: 5
    }];

    $scope.getSelectedRating = function (rating) {
        console.log(rating);
    }
}]);

app.directive('starRating', function () {
    return {
        restrict: 'A',
        template: '<ul class="rating">' +
            '<li ng-repeat="star in stars" ng-class="star" ng-click="toggle($index)">' +
            '\u2605' +
            '</li>' +
            '</ul>',
        scope: {
            ratingValue: '=',
            max: '=',
            onRatingSelected: '&'
        },
        link: function (scope, elem, attrs) {

            var updateStars = function () {
                scope.stars = [];
                for (var i = 0; i < scope.max; i++) {
                    scope.stars.push({
                        filled: i < scope.ratingValue
                    });
                }
            };

            scope.toggle = function (index) {
                scope.ratingValue = index + 1;
                scope.onRatingSelected({
                    rating: index + 1
                });
            };

            scope.$watch('ratingValue', function (oldVal, newVal) {
                if (newVal) {
                    updateStars();
                }
            });
        }
    }
});


app.controller('BarCtrl', ['$scope', function ($scope) {

    var ctx = document.getElementById("myChart");
    console.log("iamhere");
    var http = new XMLHttpRequest();
    var url = url_prefix + 'get_ratings';

    var s1 = "", s2 = "", s3 = "", s4 = "", s5 = "";

    http.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonResponse = JSON.parse(http.responseText);
            console.log(jsonResponse);

            s1 = jsonResponse['1'];
            s2 = jsonResponse['2'];
            s3 = jsonResponse['3'];
            s4 = jsonResponse['4'];
            s5 = jsonResponse['5'];
            console.log("s1:" + s1);

            var data = {
                labels: ["1", "2", "3", "4", "5"],
                datasets: [
                    {
                        label: "Stars",
                        backgroundColor: [
                            'rgba(255, 139, 90, 0.5)',
                            'rgba(255, 216, 52, 0.5)',
                            'rgba(255, 216, 52, 0.5)',
                            'rgba(173, 214, 51, 0.5)',
                            'rgba(159, 192, 90, 0.5)'
                        ],
                        borderColor: [
                            'rgba(255, 139, 90, 1)',
                            'rgba(255, 216, 52, 1)',
                            'rgba(255, 216, 52, 1)',
                            'rgba(173, 214, 51, 1)',
                            'rgba(159, 192, 90, 1)'
                        ],
                        borderWidth: 1,
                        data: [s1, s2, s3, s4, s5],
                    }
                ]
            };

            var myBarChart = new Chart(ctx, {
                type: 'bar',
                data: data,

                options: {
                    responsive: false,
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });

        }
        else if (this.status != 200) {
            // document.getElementById("card-contents").innerHTML = 'Network error!'
            console.log("error");
        }
    }
    http.open("GET", url);
    http.send();

    console.log("after req");

}]);
