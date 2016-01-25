angular.module('CardListModule', [
    'CardServiceModule',
    'CollectionServiceModule'
])
.directive('cardList', ['CardService', 'CollectionService', function (CardService, CollectionService) {
    return {
        restrict: 'A',
        scope: true,
        link: function (scope, element, attrs) {
            var initial = attrs.cardList;
            if(initial) {
                scope.cards = angular.fromJson(initial);
            } else {
                scope.loadCards();
            }
        },
        controller: ['$scope', function ($scope) {

            $scope.loadCards = function () {
                CollectionService.getCollection().then(function (response) {
                    $scope.cards = response.data;
                });
            };

            $scope.removeItem = function (id) {
                var element = document.getElementById(id);
                element.parentElement.removeChild(element);
            };

            $scope.addToCollection = function (cardName, expansion) {
                console.log('adding', cardName, expansion);
                CardService.addToCollection(cardName, expansion)
                    .then(function (response) {
                    });
            };

            $scope.deleteCard = function (id) {
                CardService.deleteCard(id).then(function () {
                    $scope.removeItem(id);
                });
            };
        }]
    };
}])
.directive('manaCost', function () {
    return {
        restrict: 'A',
        scope: {
            mana: '=manaCost'
        },
        templateUrl: '/static/js/card-list/mana-cost.html'
    };
});
