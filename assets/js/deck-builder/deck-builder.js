angular.module('DeckBuilderModule', ['CardListModule'])
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

                scope.addCard(card);
                scope.$apply();
            });
        },
        controller: ['$scope', function ($scope) {
            $scope.deck = {};
            $scope.count = 0;

            $scope.$watchCollection('deck', function (newVal) {
                $scope.colors = $scope.colorIdentity(newVal);
            });

            $scope.colorIdentity = function (deck) {
                var tmp = {},
                    identity = [];

                Object.keys(deck).forEach(function (name) {
                    var card = deck[name];
                    card.manaCost.forEach(function (mana) {
                        if(mana.color !== 'generic') {
                            if(mana.value > 0) {
                                tmp[mana.color] = 1;
                            }
                        }
                    });
                });

                Object.keys(tmp).forEach(function (name) {
                    identity.push({
                        color: name,
                        value: tmp[name]
                    });
                });

                return identity;
            };

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
