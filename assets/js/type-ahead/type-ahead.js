angular.module('TypeAheadModule', ['ManaDex'])
    .directive('typeAhead', ['PartLookupService', function (PartLookupService) {
        return {
            scope: {
                selected: '=ngModel'
            },
            restrict: 'A',
            //require: 'ngModel',
            transclude: true,
            templateUrl: '/static/js/type-ahead/type-ahead.html',
            link: function ($scope) {
                console.log($scope);
                $scope.$watch('selected', function (newVal) {
                    PartLookupService.nameTypeahead(newVal);
                });
            },
            controller: ['$scope', function ($scope) {
                $scope.results = [];
            }]
        };
    }]);
