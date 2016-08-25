'use strict';

angular.module('interfaceApp')
  .controller('SearchCtrl', function ($scope, DataService) {
    DataService.getSharedData().then(function(response){
      $scope.resources = response.resources;
    });

    this.searchVal = '';
    this.searchResults = [];

    this.SearchResources = function () {
      if(this.searchVal.length < 1){
        return;
      }
      this.searchResults = [];
      for(var i in $scope.resources){
        if($scope.resources[i].description.toLowerCase().indexOf(this.searchVal.toLowerCase()) !== -1){
          this.searchResults.push($scope.resources[i]);
        } else if($scope.resources[i].name.toLowerCase().indexOf(this.searchVal.toLowerCase()) !== -1){
          this.searchResults.push($scope.resources[i]);
        }
      }
    };
  });
