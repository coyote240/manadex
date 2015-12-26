angular.module('ManaDex', [])
    .controller('CardList', ['$scope', 'CardService', function ($scope, CardService) {
    }])
    .controller('CardForm', ['$scope', 'CardService', 'PartLookupService', '$window',
    function ($scope, CardService, PartLookupService, $window) {
        $scope.card = {
            _id: 0,
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
            CardService.createCard($scope.card).then(function () {
                $window.location.href = '/cards';
            });
        };
    }])
    .factory('CardService', ['$http', function ($http) {
        return {
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
                        id: id
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
