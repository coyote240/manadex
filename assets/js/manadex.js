angular.module('ManaDex', [
    'ManaSelectorModule',
    'TypeAheadModule',
    'CardServiceModule',
    'CardListModule'
]).filter('rarity', function () {
    var rarities = {
        common: 'Common',
        uncommon: 'Uncommon',
        rare: 'Rare',
        mythicRare: 'Mythic Rare'
    };
    return function (type) {
        type = type || 'common';
        return rarities[type];
    };
})
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
                loyalty: 0,
                expansion: null,
                type: 'creature',
                rarity: 'common',
                collectorNumber: 0,
                planeswalkerAbilities: [{
                    cost: 1,
                    rules: '',
                }, {
                    cost: 0,
                    rules: ''
                }, {
                    cost: -1,
                    rules: ''
                }]
            };


            $scope.cardsInSet = 0;
            $scope.cardTypes = {
                'creature': null,
                'legendary creature': null,
                'artifact creature': null,
                'enchantment': ['aura', 'curse', 'shrine'],
                'sorcery': ['arcane', 'trap'],
                'instant': ['arcane', 'trap'],
                'artifact': ['contraption', 'equipment', 'fortification'],
                'planeswalker': null,
                'land': null
            };

            $scope.expansions = PartLookupService.getExpansions();

            $scope.isCreatureType = function (type) {
                return /creature/i.test(type);
            };

            $scope.cardsInSet = function () {
                var expansion = $scope.expansions[$scope.card.expansion];
                if(expansion) {
                    return expansion.cardsInSet;
                } else {
                    return 0;
                }
            };

            $scope.modifiedDate = function () {
                return new Date($scope.card.lastModified.$date).toString();
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

            $scope.getTypeahead = function (current) {
                PartLookupService.nameTypeahead(current);
            };
        }
    };
}])
.factory('PartLookupService', ['$http', function ($http) {
    var expansions = {
        BFZ: {
            name: 'Battle for Zendikar',
            code: 'BFZ',
            cardsInSet: 274
        },
        OGW: {
            name: 'Oath of the Gatewatch',
            code: 'OGW',
            cardsInSet: 184
        },
        ORI: {
            name: 'Magic Origins',
            code: 'ORI',
            cardsInSet: 272
        },
        FRF: {
            name: 'Fate Reforged',
            code: 'FRF',
            cardsInSet: 185
        }
    };
    return {
        /*
         *  Needs planning, typeahead search on name field
         */
        nameTypeahead: function (query) {
            return $http.get(
                '/api/cards',
                { 
                    params: {
                        q: query
                    }
                }).then(function (response) {
                    console.log('success', response);
                    return response;
                }, function (response) {
                    console.log('error', response);
                    return response;
                });
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
