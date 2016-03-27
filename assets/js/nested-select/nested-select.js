angular.module('NestedSelectModule', [])
.directive('nestedSelect', function () {
    var colors = ['generic', 'white', 'blue', 'black', 'red', 'green', 'colorless'];
    return {
        restrict: 'A',
        require: 'ngModel',
        replace: true,
        scope: {
            color: '=ngModel'
        },
        templateUrl: '/static/js/nested-select/nested-select.html',
        link: function (scope, element, attrs) {
        },
        controller: ['$scope', function ($scope) {
            $scope.colors = colors;
            $scope.open = false;

            $scope.toggle = function () {
                $scope.open = !$scope.open;
            };

            $scope.select = function (primary, secondary) {
                $scope.open = false;
                $scope.color = primary;
            };
        }]
    };
});
