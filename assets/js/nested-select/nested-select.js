angular.module('NestedSelectModule', [])
.directive('nestedSelect', function () {
    var colors = ['white', 'blue', 'black', 'red', 'green'];
    return {
        restrict: 'A',
        require: 'ngModel',
        templateUrl: '/static/js/nested-select/nested-select.html',
        link: function (scope, element, attrs) {
        },
        controller: ['$scope', function ($scope) {
            $scope.colors = colors;

            $scope.select = function () {
                console.log(arguments);
            };
        }]
    };
});
