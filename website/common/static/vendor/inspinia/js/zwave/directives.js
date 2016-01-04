function switchContainer($interval, ZWaveDevice, ZWaveCommandClass) {
    function link(scope, element, attrs) {
        var timeoutId;
        var currentCls;
        function updateTime() {
            ZWaveDevice.query(function(devices) {
                scope.devices = devices;
            });
        }

        element.on('$destroy', function() {
            $interval.cancel(timeoutId);
        });

        scope.updateCurrentClass = function(cls, $event) {
            currentCls = cls;
        }
        element.on('change', function(e) {
            scope.updateClassWithValue(currentCls, e);
        });

        scope.switchToggle = function(cls, $event) {
            var v = ((cls.value >= '1') ? '0' : '1');
            cls.value = v;
            ZWaveCommandClass.get({id:cls.id}, function(c) {
                c.value = v.toString();
                c.$update({id:cls.id});
            });

        };
        scope.updateClassWithValue = function(cls, $event) {
            ZWaveCommandClass.get({id:cls.id}, function(c) {
                c.value = cls.value.toString();
                c.$update({id:cls.id});
            });
        };


        scope.knobOptions = {
            width: 64,
            height: 64
        };
        scope.onOff = function(cls) {
            if(cls.value == '0') {
                return false;
            } else {
                return true;
            }
        }
        updateTime();
        // start the UI update process; save the timeoutId for canceling
        // timeoutId = $interval(function() {
        //     updateTime(); // update DOM
        // }, 1000);
    }

    return {
        templateUrl: 'views/zwave/switchContainer.html',
        link: link,
        transclude: true,
        restrict: 'AEC'
    }
}

angular.module('inspinia').directive('knob', ['$timeout', function($timeout) {
    // 'use strict';

    return {
        restrict: 'EA',
        replace: true,
        template: '<input value="{{ knobData }}"/>',
        scope: {
            knobData: '=',
            knobOptions: '&'
        },
        link: function($scope, $element) {
            var knobInit = $scope.knobOptions() || {};

            knobInit.release = function(newValue) {
                $timeout(function() {
                    $scope.knobData = newValue;
                    $scope.$apply();
                });
            };

            $scope.$watch('knobData', function(newValue, oldValue) {
                if (newValue != oldValue) {
                    $($element).val(newValue).change();
                }
            });

            $($element).val($scope.knobData).knob(knobInit);
        }
    };
}]);

angular
    .module('inspinia')
    .directive('switchContainer', ['$interval',
                                   'ZWaveDevice',
                                   'ZWaveCommandClass',
                                   switchContainer])
