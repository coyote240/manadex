angular.module('ManaDex', [])
    .controller('CardForm', ['$scope', function ($scope) {
        $scope.addCard = function () {
            console.log('Adding Card');
        };
    }]);
