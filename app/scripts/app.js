'use strict';

/**
 * @ngdoc overview
 * @name interfaceApp
 * @description
 * # interfaceApp
 *
 * Main module of the application.
 */
angular
  .module('interfaceApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/search', {
        templateUrl: 'views/search.html',
        controller: 'SearchCtrl',
        controllerAs: 'resSearch'
      })
      .when('/subject/:subject_param', {
        templateUrl: 'views/subject.html',
        controller: 'SubjectCtrl',
        controllerAs: 'subject'
      })
      .when('/level/:level_param', {
        templateUrl: 'views/level.html',
        controller: 'LevelCtrl',
        controllerAs: 'level'
      })
      .when('/resource/:resource_param', {
        templateUrl: 'views/resource.html',
        controller: 'ResourceCtrl',
        controllerAs: 'resource'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
