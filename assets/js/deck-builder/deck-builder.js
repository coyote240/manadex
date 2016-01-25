angular.module('DeckBuilderModule', ['CardListModule'])
/*
.directive('deckBuilder', function () {
    return {
        scope: false,
        restrict: 'A',
        controller: ['$scope', function ($scope) {
            $scope.deck = [];

            this.addCard = function (card) {
                $scope.deck.push(card);
            };
        }]
    };
})
*/
.directive('draggable', function () {
    return {
        restrict: 'A',
        scope: false,
        link: function (scope, element, attrs) {
            element.on('dragstart', function (event) {
                var cardJson = JSON.stringify(scope.card);
                event.dataTransfer.setData('card', cardJson);
                event.dataTransfer.effectAllowed = 'move';
            });
        }
    };
})
.directive('deckList', function () {
    return {
        restrict: 'A',
        scope: true, 
        link: function (scope, element, attrs, ctrl) {

            element.on('dragover', function (event) {
                event.preventDefault();
                event.dataTransfer.dropEffect = 'move';
            });

            element.on('drop', function (event) {
                event.preventDefault();
                var data = event.dataTransfer.getData('card');
                var card = JSON.parse(data);



                //scope.deck[card.sanitized_name] = card;
                scope.addCard(card);
                scope.$apply();
            });
        },
        controller: ['$scope', function ($scope) {
            $scope.deck = {};
            $scope.count = 0;

            $scope.addCard = function (card) {
                var existing = $scope.deck[card.sanitized_name];

                if(existing) {
                    if(existing.quantity < 4) {
                        existing.quantity += 1;
                        $scope.count++;
                    }
                    return;
                }
                $scope.count++;
                card.quantity = 1;
                $scope.deck[card.sanitized_name] = card;
            };
        }]
    };
});
