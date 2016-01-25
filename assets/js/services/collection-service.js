angular.module('CollectionServiceModule', [])
.factory('CollectionService', ['$http', '$interpolate', function ($http, $interpolate) {
    return {
        getCollection: function () {
            return $http({
                method: 'GET',
                url: '/collection'
            }).then(function (response) {
                return response;
            });
        }
    };
}]);
