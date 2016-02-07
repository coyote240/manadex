angular.module('PickListModule', [])
.directive('pickList', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        templateUrl: '/static/js/pick-list/pick-list.html',
        scope: {
            selectedItems: '=ngModel',
            availableItems: '=pickList'
        },
        controller: ['$scope', function ($scope) {
            $scope.$watch('selected', function (val) {
                $scope.add(val);
            });

            $scope.add = function (item) {
                if(item && !$scope.selectedItems.includes(item)) {
                    $scope.selectedItems.push(item);
                }
            };

            $scope.remove = function (index) {
                $scope.selectedItems.splice(index, 1);
            };
        }]
    };
});
