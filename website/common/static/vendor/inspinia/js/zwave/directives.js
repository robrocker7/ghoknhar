function switchContainer($interval, ZWaveDevice) {
    function link(scope, element, attrs) {
        var timeoutId;

        function updateTime() {
            ZWaveDevice.query(function(devices) {
                scope.devices = devices;
            });
        }

        element.on('$destroy', function() {
            $interval.cancel(timeoutId);
        });

        scope.switchToggle = function(device, $event) {
            console.log(device);
        }

        // start the UI update process; save the timeoutId for canceling
        timeoutId = $interval(function() {
            updateTime(); // update DOM
        }, 1000);
    }

    return {
        templateUrl: 'views/zwave/switchContainer.html',
        link: link,
        transclude: true,
        restrict: 'AEC'
    }
}

angular
    .module('inspinia')
    .directive('switchContainer', ['$interval', 'ZWaveDevice', switchContainer])
