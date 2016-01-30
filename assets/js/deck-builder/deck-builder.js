angular.module('DeckBuilderModule', ['CardListModule'])
.controller('DeckBuilderController', ['$scope', function ($scope) {
    $scope.deck = {};

    var dereg = $scope.$watch('deckForm', function () {
        console.log($scope);
        $scope.deck.name = 'Custom Deck ' + $scope.count;
        dereg();
    });

    $scope.updateDeck = function () {
    };
}])
.factory('DeckBuilderService', ['$http', function ($http) {
    return {
        createOrUpdateDeck: function (deck) {
            var promise = deck.sanitized_name ? this.updateDeck(deck)
                                             : this.createDeck(deck);
            return promise;
        },

        createDeck: function (deck) {
            var cards = Object.keys(deck.cards).map(function (key) {
                var card = deck.cards[key];
                return {
                    sanitized_name: card.sanitized_name,
                    quantity: card.quantity
                };
            });

            return $http({
                method: 'POST',
                url: '/api/decks',
                data: {
                    name: deck.name,
                    sanitized_name: deck.sanitized_name,
                    description: deck.description,
                    cards: cards
                }
            }).then(function (response) {
                console.log('success', response);
                return response;
            }, function (response) {
                console.log('error', response);
                return response;
            });
        },

        updateDeck: function (deck, card) {
            var cards = Object.keys(deck.cards).map(function (key) {
                var card = deck.cards[key];
                return {
                    sanitized_name: card.sanitized_name,
                    quantity: card.quantity
                };
            });

            return $http({
                method: 'PUT',
                url: '/api/decks',
                data: {
                    name: deck.name,
                    sanitized_name: deck.sanitized_name,
                    description: deck.description,
                    cards: cards
                }
            }).then(function (response) {
                console.log('success', response);
                return response;
            }, function (response) {
                console.log('error', response);
                return response;
            });
        }
    };
}])
.directive('draggable', function () {
    return {
        restrict: 'A',
        scope: false,
        link: function (scope, element) {
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
        link: function (scope, element) {

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
        controller: ['$scope', 'DeckBuilderService', function ($scope, DeckBuilderService) {
            $scope.deck.cards = {};
            $scope.count = 0;

            $scope.$watchCollection('deck.cards', function (newVal) {
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
                var existing = $scope.deck.cards[card.sanitized_name];

                if(existing && existing.quantity >= 4) {
                    return;
                }

                if(existing) {
                    existing.quantity += 1;
                } else {
                    card.quantity = 1;
                    $scope.deck.cards[card.sanitized_name] = card;
                }
                $scope.count++;

                DeckBuilderService.createOrUpdateDeck($scope.deck)
                    .then(function (response) {
                        $scope.deck.sanitized_name = response.data.sanitized_name;
                    });
            };
        }]
    };
});
