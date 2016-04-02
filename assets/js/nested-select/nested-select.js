angular.module('NestedSelectModule', [])
.directive('nestedSelect', function () {
    var colors = [
        {
            label: 'generic',
            value: '{0}',
        },
        {
            label: 'white',
            value: '{W}',
            subtypes: [
                { label: 'white/blue', value: '{W/U}' },
                { label: 'white/black', value: '{W/B}' },
                { label: 'hybrid white', value: '{2/W}' }
            ]
        },
        {
            label: 'blue',
            value: '{U}',
            subtypes: [
                { label: 'blue/black', value: '{U/B}' },
                { label: 'blue/red', value: '{U/R}' },
                { label: 'hybrid blue', value: '{2/U}' }
            ]
        },
        {
            label: 'black',
            value: '{B}',
            subtypes: [
                { label: 'black/red', value: '{B/R}' },
                { label: 'black/green', value: '{B/G}' },
                { label: 'hybrid black', value: '{2/B}' }
            ]
        },
        {
            label: 'red',
            value: '{R}',
            subtypes: [
                { label: 'red/green', value: '{R/G}' },
                { label: 'red/white', value: '{R/W}' },
                { label: 'hybrid red', value: '{2/R}' }
            ]
        },
        {
            label: 'green',
            value: '{G}',
            subtypes: [
                { label: 'green/white', value: '{G/W}' },
                { label: 'green/blue', value: '{G/U}' },
                { label: 'hybrid green', value: '{2/G}' }
            ]
        },
        {
            label: 'phyrexian',
            value: '',
            subtypes: [
                { label: 'white', value: '{W/P}' },
                { label: 'blue', value: '{U/P}' },
                { label: 'black', value: '{B/P}' },
                { label: 'red', value: '{R/P}' },
                { label: 'green', value: '{G/P}' }
            ]
        },
    ];
    return {
        restrict: 'A',
        require: 'ngModel',
        replace: true,
        scope: {
            color: '=ngModel'
        },
        templateUrl: '/static/js/nested-select/nested-select.html',
        link: function (scope, element, attrs, ctrl) {
        },
        controller: ['$scope', function ($scope) {
            $scope.colors = colors;
            $scope.open = false;

            $scope.toggle = function () {
                $scope.open = !$scope.open;
            };

            $scope.select = function (value) {
                $scope.open = false;
                $scope.color.color = value;
                $scope.color.value = 1;
            };
        }]
    };
})
.filter('manaClasses', function () {
    var colorMap = {
        W: 'white',
        U: 'blue',
        B: 'black',
        R: 'red',
        G: 'green',
        P: 'phyrexian',
        2: 'hybrid'
    };
    return function (input) {
        var chars = input.split('');
        var values = chars.filter(function (c) {
            if(c in colorMap) {
                return c;
            }
        });
        return values.map(function (v) {
            return colorMap[v];
        }).join(' ');
    };
});
