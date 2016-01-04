/**
 * INSPINIA - Responsive Admin Theme
 *
 */

/**
 * MainCtrl - controller
 */
function MainCtrl($scope, $location, ZWaveDevice, ZWaveCommandClass, Auth) {


    this.userName = 'Example user';
    this.helloText = 'Welcome in SeedProject';
    this.descriptionText = 'It is an application skeleton for a typical AngularJS web app. You can use it to quickly bootstrap your angular webapp projects and dev environment for these projects.';

};

function LoginCtrl($scope, $location, api, Auth) {
        // Angular does not detect auto-fill or auto-complete. If the browser
        // autofills "username", Angular will be unaware of this and think
        // the $scope.username is blank. To workaround this we use the
        // autofill-event polyfill [4][5]
        // $('#id_auth_form input').checkAndTriggerAutoFillEvent();

        $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password};
        };

        $scope.login = function($event){
            $event.preventDefault();
            api.auth.login($scope.getCredentials()).
                $promise.
                    then(function(data){
                        // on good username and password
                        Auth.setUser(data);
                        $location.path('/index')
                    }).
                    catch(function(data){
                        // on incorrect username and password
                        alert(data.data.detail);
                    });
        };

        $scope.logout = function(){
            api.auth.logout(function(){
                Auth.setUser(undefined);
            });
        };
    };

    // $scope.login = function () {
    // // Ask to the server, do your job and THEN set the user
    //     Auth.setUser(user); //Update the state of the user in the app
    // };

angular
    .module('inspinia')
    .controller('MainCtrl', ['$scope', '$location', 'ZWaveDevice', 'ZWaveCommandClass', 'Auth', MainCtrl])
    .controller('loginCtrl', [ '$scope', '$location', 'api', 'Auth', LoginCtrl]);
