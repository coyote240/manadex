angular.module('CardServiceModule', [])
.factory('CardService', ['$http', '$interpolate', function ($http, $interpolate) {
    var addToCollectionUrl = $interpolate('/collection/{{ expansion }}/{{ cardName }}');

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
        },

        addToCollection: function (name, expansion) {
            var url = addToCollectionUrl({
                    cardName: name,
                    expansion: expansion});
            console.log('at service', url);
            return $http({
                method: 'POST',
                url: url
            }).then(function (response) {
                console.log('success', response);
            }, function (response) {
                console.log('error', response);
            });
        }
    };
}])
.factory('PartLookupService', ['$http', function ($http) {

    var keywords = [
        'activate', 'attach', 'cast', 'counter', 'deathtouch', 'defender',
        'destroy', 'discard', 'double strike', 'enchant', 'equip', 'exchange',
        'exile', 'fight', 'first strike', 'flash', 'flying', 'haste',
        'hexproof', 'indestructible', 'lifelink', 'menace', 'play', 'prowess',
        'reach', 'regenerate', 'reveal', 'sacrifice', 'scry', 'search',
        'shuffle', 'tap/untap', 'trample', 'vigilance'];

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
            return $http({
                method: 'GET',
                url: '/api/cards/expansions'
            });
        },

        /*
         *  May go into DB so to store current vs. former
         *  http://mtgsalvation.gamepedia.com/Evergreen
         */
        getEvergreenKeywords: function () {
            return keywords;
        }
    };
}]);
