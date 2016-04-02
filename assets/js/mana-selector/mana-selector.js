angular.module('ManaSelectorModule', [])
    .directive('manaSelector', [function () {
        return {
            scope: {
                mana: '=ngModel'
            },
            restrict: 'A',
            require: 'ngModel',
            templateUrl: '/static/js/mana-selector/mana-selector.html',
            link: function () {
            },
            controller: ['$scope', function ($scope) {
                $scope.mana = $scope.mana || [{
                    color: 'generic',
                    value: 0
                }];

                $scope.addMana = function ($event) {
                    $event.preventDefault();

                    $scope.mana.push({
                        color: 'generic',
                        value: 0
                    });
                };

                $scope.removeMana = function ($event, $index) {
                    $event.preventDefault();

                    $scope.mana.splice($index, 1);
                };
            }]
        };
    }]);
