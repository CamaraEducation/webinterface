/*
Controller for the Search view. Fetches data and can search through it.
*/
'use strict';

angular.module('interfaceApp')
  .controller('SearchCtrl', function ($scope, DataService) {
    //As usual, gotta get the data
    DataService.getSharedData().then(function(response){
      $scope.resources = response.resources;
    });

    this.searchVal = '';
    this.searchResults = [];
    this.searchedYet = false;   //Want to track if a search has been performed yet, to know whether to display "No results found" or not.

    //Fairly simple search function. Not optimised, doesn't sort results by most relevant.
    this.SearchResources = function () {
      this.searchedYet = true;
      this.searchResults = [];
      if(this.searchVal.length < 1){
        //Will not search for an empty string
        return;
      }
      //Checks for search term in both description and name of each resource. Case-insensitive.
      for(var i in $scope.resources){
        if($scope.resources[i].description.toLowerCase().indexOf(this.searchVal.toLowerCase()) !== -1){
          this.searchResults.push($scope.resources[i]);
        } else if($scope.resources[i].name.toLowerCase().indexOf(this.searchVal.toLowerCase()) !== -1){
          this.searchResults.push($scope.resources[i]);
        }
      }
    };
  });
