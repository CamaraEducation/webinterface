'use strict';

angular.module('interfaceApp')
  .controller('ResourceCtrl', function ($scope, $http, $routeParams, DataService) {

    $scope.current_resource = [];
    $scope.current_resource.name = $routeParams.resource_param;

    DataService.getSharedData().then(function(response){
      for(var i in response.resources){
        if(response.resources[i].name === $scope.current_resource.name){
          $scope.current_resource = response.resources[i];
        }
      }
    });
});
