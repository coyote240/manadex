angular.module('ManaDex', [])
    .controller('CardForm', ['$scope', function ($scope) {
        $scope.cardsInSet = 0;
        $scope.cardTypes = ['creature', 'enchantment', 'sorcery', 'instant',
                            'artifact', 'planeswalker', 'land'];

        $scope.addCard = function () {
            console.log('Adding Card');
        };
    }])
    .factory('PartLookupService', ['$http', function ($http) {
        return {
            getExpansions: function () {
            },

            getEvergreenKeywords: function () {
            }
        };
    }]);
