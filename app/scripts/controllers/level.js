'use strict';

angular.module('interfaceApp')
  .controller('LevelCtrl', function ($scope, $http, $routeParams, DataService) {

  $scope.current_level = [];
  $scope.current_level.name = $routeParams.level_param;
  $scope.level_software = {};

  DataService.getSharedData().then(function(response){
    $scope.level_list = response.levels;

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
