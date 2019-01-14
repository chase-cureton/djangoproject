(function() {
  'use strict';

  angular.module('djangoproject', [
    'djangoproject.config',
    'djangoproject.routes',
    'djangoproject.authentication'
  ]);

  angular.module('djangoproject.routes', ['ngRoute']);

  angular.module('djangoproject.config', []);

  //Used to handle CSRF protection
  angular.module('djangoproject')
         .run(run);

  run.$inject = ['$http'];

  /**
   * @name run
   * @desc Update xsrf $http headers to align with Django's defaults
   */
  function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrfToken';
  }
})();