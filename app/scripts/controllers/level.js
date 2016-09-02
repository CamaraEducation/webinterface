/*
Controller to handle the Level view. Quite simple, just populates the lists of subjects for each educational level
*/
'use strict';

angular.module('interfaceApp')
  .controller('LevelCtrl', function ($scope, $http, $routeParams, DataService) {

  $scope.current_level = [];
  $scope.current_level.name = $routeParams.level_param;
  $scope.level_software = {};

  //Get the resource & subject data
  DataService.getSharedData().then(function(response){
    $scope.level_list = response.levels;
    //Sort the subject into the levels that contain resources for that subject
    for(var i in response.resources){
      if(response.resources[i].level.indexOf($scope.current_level.name) >= 0){
        if(!$scope.level_software.hasOwnProperty(response.resources[i].category)){
          var j=0;
          var max = response.subjects.length;
          var not_found = true;
          while(not_found && (j<max)){
            if(response.subjects[j].name === response.resources[i].category){
              not_found = false;
              $scope.level_software[response.resources[i].category] = response.subjects[j];
              $scope.level_software[response.resources[i].category].resources = [];
            }
            j++;
          }
        }
        $scope.level_software[response.resources[i].category].resources.push(response.resources[i]);
      }
    }
  });
});
