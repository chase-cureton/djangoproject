/**
 * Register controller
 * @namespace djangoproject.authentication.controllers
 */

 (function(){
    'use strict';

    //Registering controller
    angular.module('djangoproject.authentication.controllers')
           .controller('RegisterController', RegisterController)

    RegisterController.$inject = ['$location', '%scope', 'Authentication']

    /**
     * @namespace RegisterController
     */
    function RegisterController($location, $scope, Authentication) {
        var vm = this;

        vm.register = register;

        /**
         * @name register
         * @desc Register a new user
         * @memberof djangoproject.authentication.controllers.RegisterController
         */
        function register() {
            Authentication.register(vm.email, vm.password, vm.username);
        }
    }
 })();