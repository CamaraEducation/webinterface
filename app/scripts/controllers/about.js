'use strict';

angular.module('interfaceApp')
  .controller('AboutCtrl', function ($scope, DataService) {
    DataService.getSharedData().then(function(response){
      $scope.resources = response.resources;
    });

    this.searchVal = '';
    this.searchResults = [];

    this.SearchResources = function () {
      console.log('SEARCHING FOR ' + this.searchVal);
      if(this.searchVal.length < 1){
        console.log('TOO SHORT');
        return;
      }
      this.searchResults = [];
      for(var i in $scope.resources){
        if($scope.resources[i].description.toLowerCase().indexOf(this.searchVal.toLowerCase()) !== -1){
          this.searchResults.push($scope.resources[i]);
        }
      }
      console.log(this.searchResults);
    };
  });
