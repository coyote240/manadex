angular.module('CardListModule', ['CardServiceModule'])
    .controller('CardList', ['$scope', 'CardService', '$document', function ($scope, CardService, $document) {
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
    }]);
