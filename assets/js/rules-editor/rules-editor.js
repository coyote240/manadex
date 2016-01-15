angular.module('RulesEditorModule', [])
    .directive('rulesEditor', function () {
        return {
            scope: {
            },
            restrict: 'A',
            require: 'ngModel',
            templateUrl: '/static/js/rules-editor/rules-editor.html',
            controller: ['$scope', function ($scope) {
            }]
        };
    });
