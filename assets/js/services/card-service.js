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
    }]);
