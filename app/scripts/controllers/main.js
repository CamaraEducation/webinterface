'use strict';

/**
 * @ngdoc function
 * @name interfaceApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the interfaceApp
 */
angular.module('interfaceApp')
  .controller('MainCtrl', function ($scope, $http, DataService) {

    DataService.getSharedData().then(function(response){
      $scope.subject_list = response.subjects;
      $scope.level_list = response.levels;
    });
  })

  .service('DataService', function($http, $q){
    var shared_data = [];
    shared_data.subjects = [];
    shared_data.levels = [];
    shared_data.resources = [];

    return {
      getSharedData: function(){
        var deferred_data = $q.defer();
        if(shared_data.subjects.length > 0){
          deferred_data.resolve(shared_data);
        } else {
          $http.get('/resources/software_list.json').then(function(response){
            shared_data.subjects = response.data.subjects;
            shared_data.levels = response.data.levels;
            shared_data.resources = response.data.resources;

            deferred_data.resolve(response.data);
          });
        }
        return deferred_data.promise;
      },
      setSharedData: function(value){
        shared_data = value;
      }
    };
  });
