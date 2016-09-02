/*
A controller for the resource view.
Doesn't do much, doesn't need to. It just finds the full information about the resource in question
*/
'use strict';

angular.module('interfaceApp')
  .controller('ResourceCtrl', function ($scope, $http, $routeParams, DataService) {

    $scope.current_resource = {};
    $scope.current_resource.name = $routeParams.resource_param;

    //Get all the data
    DataService.getSharedData().then(function(response){
      //Find the one relevant resource
      for(var i in response.resources){
        if(response.resources[i].name === $scope.current_resource.name){
          $scope.current_resource = response.resources[i];
        }
      }
    });
});
