angular.module('inspinia')
    .factory('ZWaveDevice', ['$resource', function($resource) {
        return $resource('/api/zwave/device/:id/', null,
            {
                'update': { method:'PUT' },
            }, {
                'stripTrailingSlashes': false
            });
    }]);

angular.module('inspinia')
    .factory('ZWaveCommandClass', ['$resource', function($resource) {
        return $resource('/api/zwave/command-class/:id/', null,
            {
                'update': { method:'PUT'},
            }, {
                'stripTrailingSlashes': false
            });
    }]);
angular.module('inspinia')
    .factory('api', function($resource){
        function add_auth_header(data, headersGetter){
            // as per HTTP authentication spec [1], credentials must be
            // encoded in base64. Lets use window.btoa [2]
            var headers = headersGetter();
            headers['Authorization'] = ('Basic ' + btoa(data.username +
                                        ':' + data.password));
        }
        // defining the endpoints. Note we escape url trailing dashes: Angular
        // strips unescaped trailing slashes. Problem as Django redirects urls
        // not ending in slashes to url that ends in slash for SEO reasons, unless
        // we tell Django not to [3]. This is a problem as the POST data cannot
        // be sent with the redirect. So we want Angular to not strip the slashes!
        return {
            auth: $resource('/api/auth\\/', {}, {
                get: {method: 'GET'},
                login: {method: 'POST', transformRequest: add_auth_header},
                logout: {method: 'DELETE'}
            })
        }
    });

angular.module('inspinia')
    .factory('Auth', ['api', function(api) {
        var user, initCheck;

        return{
            setUser : function(aUser){
                user = aUser;
            },
            getUser: function() {
                return user;
            },
            isLoggedIn : function() {
                if(!user && !initCheck) {
                    api.auth.get(function(response) {
                        user = response;
                        return user;
                    }, function() {
                        return user;
                    });
                    initCheck = true;
                } else {
                    return(user)? user : false;
                }
            }
        }
    }]);
