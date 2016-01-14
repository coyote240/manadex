angular.module('ManaDex', ['ManaSelectorModule'])
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
                    expansion: null,
                    type: 'creature',
                    rarity: 'common',
                    collectorNumber: 0
                };

                $scope.cardsInSet = 0;
                $scope.cardTypes = ['creature', 'enchantment', 'sorcery', 'instant',
                                    'artifact', 'planeswalker', 'land'];

                $scope.expansions = PartLookupService.getExpansions();

                $scope.cardsInSet = function () {
                    var expansion = $scope.expansions[$scope.card.expansion];
                    if(expansion) {
                        return expansion.cardsInSet;
                    } else {
                        return 0;
                    }
                };

                $scope.addCard = function () {
                    if($scope.cardForm.$invalid) {
                        return false;
                    }
                    CardService.createOrUpdateCard($scope.card).then(function () {
                        $window.location.href = '/cards';
                    }, function (response) {
                        console.log(response);
                    });
                };
            }
        };
    }])
    .factory('CardService', ['$http', function ($http) {
        return {
            createOrUpdateCard: function (card) {
                var promise = card.sanitized_name ? this.updateCard(card) : this.createCard(card);
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

            deleteCard: function (sanitized_name) {
                return $http({
                    method: 'DELETE',
                    url: '/api/cards',
                    data: {
                        sanitized_name: sanitized_name 
                    }
                }).then(function (response) {
                    console.log('success', response);
                }, function (response) {
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
