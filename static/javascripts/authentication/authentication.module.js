(function(){
    'use strict';

    //Defines module with dependencies
    angular.module('djangoproject.authentication', [
                   'djangoproject.authentication.controllers',
                   'djangoproject.authentication.services'
    ]);

    //Defines modules with no dependencies
    angular.module('djangoproject.authentication.controllers', []);

    angular.module('djangoproject.authentication.services', []);
})();