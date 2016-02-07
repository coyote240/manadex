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
                type: 'creature',
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
                keywords: []
            };


            $scope.cardsInSet = 0;
            $scope.cardTypes = {
                'creature': null,
                'artifact creature': null,
                'enchantment': ['aura', 'curse', 'shrine'],
                'sorcery': ['arcane', 'trap'],
                'instant': ['arcane', 'trap'],
                'artifact': ['contraption', 'equipment', 'fortification'],
                'planeswalker': null,
                'land': ['plains', 'island', 'swamp', 'mountain', 'forest'] 
            };
            $scope.supertypes = ['basic', 'elite', 'legendary', 'ongoing',
                                 'snow', 'world'];

            $scope.expansions = PartLookupService.getExpansions();
            $scope.evergreen = PartLookupService.getEvergreenKeywords();

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
}]);
