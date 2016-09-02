/*
Controller for Subject view. Just populates software list for a given subject.
*/
'use strict';

angular.module('interfaceApp')
  .controller('SubjectCtrl', function ($scope, $http, $routeParams, DataService) {

  $scope.current_subject = [];
  $scope.current_subject.name = $routeParams.subject_param;
  $scope.subject_software = [];

  //Step 1: get the data
  DataService.getSharedData().then(function(response){
    $scope.subject_list = response.subjects;

    //Step 2: check if the resource's subject is the subject in question
    for(var i in response.resources){
      if(response.resources[i].category === $scope.current_subject.name){
        $scope.subject_software.push(response.resources[i]);
      }
    }
  });
});
