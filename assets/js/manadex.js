angular.module('ManaDex', [])
    .controller('CardForm', ['$scope', function ($scope) {
        $scope.card = {
            power: 0,
            toughness: 0,
            type: 'creature',
            rarity: 'common'
        };
        $scope.cardsInSet = 0;
        $scope.cardTypes = ['creature', 'enchantment', 'sorcery', 'instant',
                            'artifact', 'planeswalker', 'land'];

        $scope.addCard = function () {
            console.log('Adding Card');
            console.log($scope.card);
        };
    }])
    .factory('PartLookupService', ['$http', function ($http) {
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
            },

            /*
             *  May go into DB so to store current vs. former
             *  http://mtgsalvation.gamepedia.com/Evergreen
             */
            getEvergreenKeywords: function () {
            }
        };
    }]);
