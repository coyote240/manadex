angular.module('CardFormModule',
    ['ManaSelectorModule', 'TypeAheadModule', 'CardServiceModule', 'PickListModule'])
.directive('cardForm', ['CardService', 'PartLookupService', '$window', 
function (CardService, PartLookupService, $window) {
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
                types: [],
                rarity: 'common',
                collectorNumber: 0,
                abilities: [{
                    cost: 1,
                    rules: '',
                }, {
                    cost: 0,
                    rules: ''
                }, {
                    cost: -1,
                    rules: ''
                }],
                keywords: [],
                inMyCollection: true
            };


            $scope.cardsInSet = 0;
            $scope.cardTypes = ['creature', 'artifact', 'enchantment',
                                'sorcery', 'instant', 'planeswalker', 'land'];
            $scope.supertypes = ['basic', 'elite', 'legendary', 'ongoing',
                                 'snow', 'world'];

            $scope.expansions = {};
            var expansionsLookup = {};

            PartLookupService.getExpansions()
                .then(function success (response) {
                    $scope.expansions = response.data;
                    $scope.expansions.forEach(function (set) {
                        expansionsLookup[set.code] = set;
                    });
                });

            $scope.evergreen = PartLookupService.getEvergreenKeywords();

            $scope.selectExpansion = function (code) {
                var set = expansionsLookup[code];
                $scope.cardsInSet = set ? set.size : 0;
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
}]);
