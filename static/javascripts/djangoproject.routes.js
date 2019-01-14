(function () {
    'use strict';
  
    angular
      .module('djangoproject.routes')
      .config(config);
  
    //Injecting route provider as a dependency for config, which will allow to add routing to the client
    config.$inject = ['$routeProvider'];
  
    /**
    * @name config
    * @desc Define valid application routes
    */
    function config($routeProvider) {
      $routeProvider.when('/register', {
        controller: 'RegisterController', 
        controllerAs: 'vm',
        templateUrl: '/static/templates/authentication/register.html'
      }).otherwise('/');
    }
  })();