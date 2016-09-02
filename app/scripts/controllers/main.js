'use strict';

/**
 * @ngdoc function
 * @name interfaceApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the interfaceApp
 */
 /*
Controller for the front page of the web app. Mainly just for populating data structures
 */
angular.module('interfaceApp')
  .controller('MainCtrl', function ($scope, $http, DataService) {
    //Populates the level and subject lists
    DataService.getSharedData().then(function(response){
      $scope.subject_list = response.subjects;
      $scope.level_list = response.levels;
    });
  })

  //Service that stores or fetches the resource data
  .service('DataService', function($http, $q){
    var shared_data = [];
    shared_data.subjects = [];
    shared_data.levels = [];
    shared_data.resources = [];

    return {
      getSharedData: function(){
        /*Using a promise here creates a way for controllers that call this function and
        wait on the response before executing code that depends on that response*/
        var deferred_data = $q.defer();
        //If the data has already been fetched before, send it back straight away
        if(shared_data.subjects.length > 0){
          deferred_data.resolve(shared_data);
        } else {
          //Otherwise fetch the json file
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
