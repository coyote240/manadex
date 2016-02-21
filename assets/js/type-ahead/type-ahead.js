angular.module('TypeAheadModule', ['CardServiceModule'])
.directive('typeAhead', ['PartLookupService', function (PartLookupService) {
    return {
        scope: {
            name: '=ngModel'
        },
        restrict: 'E',
        require: 'ngModel',
        transclude: true,
        templateUrl: '/static/js/type-ahead/type-ahead.html',
        link: function (scope, element) {
            var selectedIndex = 0;

            scope.$watch('name', function (newVal) {
                if(!newVal) {
                    scope.results = [];
                    return;
                }
                PartLookupService.nameTypeahead(newVal).then(function (response) {
                    scope.results = response.data.results;
                    selectedIndex = 0;
                    scope.results[selectedIndex].selected = true;
                });
            });

            element.on('keyup', function (event) {
                var key = event.key;
                event.preventDefault();

                if(key === 'ArrowDown') {
                    selectedIndex++;
                    scope.hiliteRow(selectedIndex);
                } else if (key === 'ArrowUp') {
                    selectedIndex = selectedIndex ? selectedIndex - 1 : 0;
                    scope.hiliteRow(selectedIndex);
                } else if (key === 'Enter') {
                    // Fill-out form
                } else if (key === 'Escape') {
                    scope.reset();
                }


            });

            var input = element.find('input');
            input.on('blur', function () {
                scope.reset();
            });
        },
        controller: ['$scope', function ($scope) {
            $scope.results = [];

            $scope.hiliteRow = function (index) {
                var selected = $scope.results[index];

                $scope.results.forEach(function (current) {
                    current.selected = false;
                });

                if(selected) {
                    selected.selected = true;
                    $scope.$apply();
                }
            };

            $scope.reset = function () {
                $scope.results = [];
                $scope.$apply();
            };
        }]
    };
}]);
