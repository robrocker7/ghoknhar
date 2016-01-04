/**
 * INSPINIA - Responsive Admin Theme
 *
 * Inspinia theme use AngularUI Router to manage routing and views
 * Each view are defined as state.
 * Initial there are written state for all view in theme.
 *
 */
function config($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $httpProvider) {
    $urlRouterProvider.otherwise("/index/main");

    $ocLazyLoadProvider.config({
        // Set to true if you want to see what and when is dynamically loaded
        debug: false
    });

    $stateProvider

        .state('index', {
            abstract: true,
            url: "/index",
            templateUrl: "views/common/content.html",
        })
        .state('index.switches', {
            url: "/main",
            templateUrl: "views/main.html",
            data: { pageTitle: 'Ghoknhar Network Switches' }
        })
        .state('index.meters', {
            url: "/minor",
            templateUrl: "views/minor.html",
            data: { pageTitle: 'Ghoknhar Network Meters' }
        })
        .state('login', {
            url: "/login",
            templateUrl: "views/zwave/loginView.html"
        })

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}
angular
    .module('inspinia')
    .config(config)
    .run(['$rootScope', '$location', 'Auth', function ($rootScope, $location, Auth) {
        $rootScope.$on('$routeChangeStart', function (event) {
            if (!Auth.isLoggedIn()) {
                event.preventDefault();
                $location.path('/login');
            }
        });
    }])
    .run(['$rootScope', '$state', '$location', 'Auth', function($rootScope, $state, $location, Auth) {
        $rootScope.$state = $state;
        $rootScope.$watch(Auth.isLoggedIn, function (value, oldValue) {
            if((!value && oldValue) || (!value && !oldValue)) {
              console.log("Disconnect");
              $location.path('/login');
            }else if(value) {
              console.log("Connect");
              $location.path('/index');
            }
            $rootScope.user = Auth.getUser();
        }, true);
    }]);
