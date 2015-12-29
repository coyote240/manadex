angular.module('ManaDex', [])
    .controller('CardList', ['$scope', 'CardService', '$document', function ($scope, CardService, $document) {
        $scope.removeItem = function (id) {
            var element = document.getElementById(id);
            element.parentElement.removeChild(element);
        };

        $scope.deleteCard = function (id) {
            CardService.deleteCard(id).then(function () {
                $scope.removeItem(id);
            });
        };
    }])
    .directive('cardForm', ['CardService', 'PartLookupService', '$window', function (CardService, PartLookupService, $window) {

        /* TODO:
         * If _id is zero, create
         * else update.
         *
         * Setting the expansion doesn't update cards in set count.
         *
         * Get the mana selectors under control
         * Perhaps a directive?  How to show color?
         *
         * Should only show validation on submit
         */

        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                var card = JSON.parse(attrs.cardForm, '{}');
                angular.extend(scope.card, card);
            },
            controller: function ($scope, $element, $attrs) {
                $scope.card = {
                    power: 0,
                    toughness: 0,
                    type: 'creature',
                    rarity: 'common',
                    collectorNumber: 0
                };

                $scope.cardsInSet = 0;
                $scope.cardTypes = ['creature', 'enchantment', 'sorcery', 'instant',
                                    'artifact', 'planeswalker', 'land'];

                $scope.expansions = PartLookupService.getExpansions();

                $scope.updateCardsInSet = function () {
                    $scope.cardsInSet = $scope.expansions[$scope.card.expansion].cardsInSet;
                };

                $scope.addCard = function () {
                    if($scope.cardForm.$invalid) {
                        return false;
                    }
                    CardService.createOrUpdateCard($scope.card).then(function () {
                        $window.location.href = '/cards';
                    });
                };
            }
        };
    }])
    .factory('CardService', ['$http', function ($http) {
        return {
            createOrUpdateCard: function (card) {
                console.log('create or update', card);
                var promise = card._id ? this.createCard(card) : this.updateCard(card);
                return promise;
            },

            createCard: function (card) {
                return $http({
                    method: 'POST',
                    url: '/api/cards',
                    data: card
                }).then(function (response) {
                    console.log('success', response);
                    return response;
                }, function (response) {
                    console.log('error', response);
                    return response;
                });
            },

            updateCard: function (card) {
                return $http({
                    method: 'PUT',
                    url: '/api/cards',
                    data: card
                }).then(function (response) {
                    console.log('success', response);
                }, function (response) {
                    console.log('error', response);
                });
            },

            deleteCard: function (id) {
                return $http({
                    method: 'DELETE',
                    url: '/api/cards',
                    data: {
                        _id: id
                    }
                }).then(function (response) {
                    console.log('success', response);
                }, function () {
                    console.log('error', response);
                });
            }
        };
    }])
    .factory('PartLookupService', ['$http', function ($http) {
        var expansions = {
            ORI: {
                name: 'Magic Origins',
                code: 'ORI',
                cardsInSet: 272
            },
            BFZ: {
                name: 'Battle for Zendikar',
                code: 'BFZ',
                cardsInSet: 274
            }};
        return {
            /*
             *  Needs planning, typeahead search on name field
             */
            nameTypeahead: function () {
            },

            /*
             *  Typeahead for known subtypes
             */
            subtypeTypeahead: function () {
            },

            /*
             *  Expansions is a big bit of info with a lot of attributes.
             *  Will put into DB
             *  http://mtgsalvation.gamepedia.com/Expansion#List_of_Magic_expansions_and_sets
             */
            getExpansions: function () {
                return expansions;
            },

            /*
             *  May go into DB so to store current vs. former
             *  http://mtgsalvation.gamepedia.com/Evergreen
             */
            getEvergreenKeywords: function () {
            }
        };
    }]);
