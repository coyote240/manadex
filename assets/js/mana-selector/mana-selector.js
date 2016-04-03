angular.module('ManaSelectorModule', [])
.directive('manaSelector', function () {
    var parsePattern = new RegExp('({[\\dWUBRGCX]+\\/*[WUBRGP]*})', 'g');
    return {
        scope: {
            mana: '=ngModel'
        },
        restrict: 'A',
        require: 'ngModel',
        templateUrl: '/static/js/mana-selector/mana-selector.html',
        link: function (scope, element, attrs, ctrl) {
            scope.manaValues = scope.mana.match(parsePattern).map(function (current) {
                return {
                    val: current
                };
            });
            scope.$watch('manaValues', function (newVal) {
                scope.mana = newVal.map(function (current) {
                    return current.val;
                }).join('');
            }, true);
        },
        controller: ['$scope', function ($scope) {
            $scope.mana = $scope.mana || '{0}';

            $scope.addMana = function ($event) {
                $event.preventDefault();

                $scope.manaValues.push({
                    val: '{0}'
                });
            };

            $scope.removeMana = function ($event, $index) {
                $event.preventDefault();

                $scope.manaValues.splice($index, 1);
            };
        }]
    };
});
