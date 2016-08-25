'use strict';

angular.module('interfaceApp')
  .controller('SubjectCtrl', function ($scope, $http, $routeParams, DataService) {

  $scope.current_subject = [];
  $scope.current_subject.name = $routeParams.subject_param;
  $scope.subject_software = [];

  DataService.getSharedData().then(function(response){
    $scope.subject_list = response.subjects;

    for(var i in response.resources){
      if(response.resources[i].category === $scope.current_subject.name){
        $scope.subject_software.push(response.resources[i]);
      }
    }
  });
});
