angular.module('NestedSelectModule', [])
.directive('nestedSelect', function () {
    var colors = ['generic', 'white', 'blue', 'black', 'red', 'green', 'colorless'];
    return {
        restrict: 'A',
        require: 'ngModel',
        scope: {
            color: '=ngModel'
        },
        templateUrl: '/static/js/nested-select/nested-select.html',
        link: function (scope, element, attrs) {
        },
        controller: ['$scope', function ($scope) {
            $scope.colors = colors;

            $scope.select = function (primary, secondary) {
                console.log([primary, secondary].join(', '));
            };
        }]
    };
});
