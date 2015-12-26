angular.module('inspinia')
    .factory('ZWaveDevice', ['$resource', function($resource) {
        return $resource('/api/zwave/device/:id', null,
            {
                'update': { method:'PUT' }
            });
    }]);
