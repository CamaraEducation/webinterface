"use strict";angular.module("interfaceApp",["ngAnimate","ngCookies","ngResource","ngRoute","ngSanitize","ngTouch"]).config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl",controllerAs:"main"}).when("/about",{templateUrl:"views/about.html",controller:"AboutCtrl",controllerAs:"about"}).when("/subject/:subject_param",{templateUrl:"views/subject.html",controller:"SubjectCtrl",controllerAs:"subject"}).when("/level/:level_param",{templateUrl:"views/level.html",controller:"LevelCtrl",controllerAs:"level"}).when("/resource/:resource_param",{templateUrl:"views/resource.html",controller:"ResourceCtrl",controllerAs:"resource"}).otherwise({redirectTo:"/"})}]),angular.module("interfaceApp").controller("MainCtrl",["$scope","$http","DataService",function(a,b,c){c.getSharedData().then(function(b){a.subject_list=b.subjects,a.level_list=b.levels})}]).service("DataService",["$http","$q",function(a,b){var c=[];return c.subjects=[],c.levels=[],c.resources=[],{getSharedData:function(){var d=b.defer();return c.subjects.length>0?d.resolve(c):a.get("/resources/software_list.json").then(function(a){c.subjects=a.data.subjects,c.levels=a.data.levels,c.resources=a.data.resources,d.resolve(a.data)}),d.promise},setSharedData:function(a){c=a}}}]),angular.module("interfaceApp").controller("AboutCtrl",function(){this.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"]}),angular.module("interfaceApp").controller("SubjectCtrl",["$scope","$http","$routeParams","DataService",function(a,b,c,d){a.current_subject=[],a.current_subject.name=c.subject_param,a.subject_software=[],d.getSharedData().then(function(b){a.subject_list=b.subjects;for(var c in b.resources)b.resources[c].category===a.current_subject.name&&a.subject_software.push(b.resources[c])})}]),angular.module("interfaceApp").controller("ResourceCtrl",["$scope","$http","$routeParams","DataService",function(a,b,c,d){a.current_resource=[],a.current_resource.name=c.resource_param,d.getSharedData().then(function(b){for(var c in b.resources)b.resources[c].name===a.current_resource.name&&(a.current_resource=b.resources[c])})}]),angular.module("interfaceApp").controller("LevelCtrl",["$scope","$http","$routeParams","DataService",function(a,b,c,d){a.current_level=[],a.current_level.name=c.level_param,a.level_software={},d.getSharedData().then(function(b){a.level_list=b.levels;for(var c in b.resources)if(b.resources[c].level.indexOf(a.current_level.name)>=0){if(!a.level_software.hasOwnProperty(b.resources[c].category))for(var d=0,e=b.subjects.length,f=!0;f&&e>d;)b.subjects[d].name===b.resources[c].category&&(f=!1,a.level_software[b.resources[c].category]=b.subjects[d],a.level_software[b.resources[c].category].resources=[]),d++;a.level_software[b.resources[c].category].resources.push(b.resources[c])}})}]),angular.module("interfaceApp").run(["$templateCache",function(a){a.put("views/about.html","<p>This is the about view.</p>"),a.put("views/level.html",'<div class="row marketing"> <h2>Resources for {{current_level.name}}</h2> <div class="well" ng-repeat="subject in level_software"> <h3>{{subject.name}}</h3> <hr> <a class="btn btn-row" ng-repeat="resource in subject.resources" href="#/resource/{{resource.name}}"><img ng-src="images/app_icons/{{resource.icon}}"><p>{{resource.name}}</p></a> </div> </div>'),a.put("views/main.html",'<div class="jumbotron"> <h2>Welcome to the Camara Resource Compendium</h2> <p> <img src="images/interface_icons/Symbolsmall.png" alt="Camara"><br> Information on all educational resources is compiled here. </p> </div> <div class="row marketing"> <div class="well"> <h3>Resources by subject:</h3> <hr> <a class="btn btn-row" ng-repeat="subject in subject_list" href="#/subject/{{subject.name}}"><img ng-src="images/interface_icons/{{subject.icon}}"><p>{{subject.name}}</p></a> </div> <div class="well"> <h3>Resources by age range:</h3> <hr> <a class="btn btn-row" ng-repeat="level in level_list" href="#/level/{{level.name}}"><img ng-src="images/interface_icons/{{level.icon}}"><p>{{level.name}}</p></a> </div> </div>'),a.put("views/resource.html",'<div class="well"> <h2><img ng-src="images/app_icons/{{current_resource.icon}}">{{current_resource.name}}</h2> </div> <div class="well"> <img class="screenshot" src="/images/app_screenshots/{{current_resource.screenshot}}" alt="{{current_resource.name}}"> <div class="aside">{{current_resource.description}}</div> </div>'),a.put("views/subject.html",'<div class="row marketing"> <div class="well"> <h3>Resources for {{current_subject.name}} <hr> <a class="btn btn-row" ng-repeat="resource in subject_software" href="#/resource/{{resource.name}}"><img ng-src="images/app_icons/{{resource.icon}}"><p>{{resource.name}}</p></a> </h3></div> </div>')}]);