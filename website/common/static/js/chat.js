;
(function ($, window, document, undefined) {

    // undefined is used here as the undefined global
    // variable in ECMAScript 3 and is mutable (i.e. it can
    // be changed by someone else). undefined isn't really
    // being passed in so we can ensure that its value is
    // truly undefined. In ES5, undefined can no longer be
    // modified.

    // window and document are passed through as local
    // variables rather than as globals, because this (sligshtly)
    // quickens the resolution process and can be more
    // efficiently minified (especially when both are
    // regularly referenced in your plugin).

    // Create the defaults once
    var pluginName = "castillochat",
        defaults = {
            alias: ""
        };

    // The actual plugin constructor
    function Plugin(element, options) {
        this.element = element;

        // jQuery has an extend method that merges the
        // contents of two or more objects, storing the
        // result in the first object. The first object
        // is generally empty because we don't want to alter
        // the default options for future instances of the plugin
        this.options = $.extend({}, defaults, options);
        this.message_obj = $('<div class="media"><div class="media-left"><a href="#"><img src="http://placehold.it/35x35" class="media-object"></a></div><div class="media-body"><div class="media-heading"></div><p></p></div></div>');
        this._defaults = defaults;
        this._name = pluginName;
        this.socket = null;
        this.init();
    }

    Plugin.prototype = {

        init: function () {
            // Place initialization logic here
            // You already have access to the DOM element and
            // the options via the instance, e.g. this.element
            // and this.options
            // you can add more functions like the one below and
            // call them like so: this.yourOtherFunction(this.element, this.options).

            var $el = $(this.element);
            var elements = ['#message_container', '#message_input', '#message_send'];
            $.each(elements, function(i) {
                if(!$(this).length) {
                    console.error('Element $(' + this + ') not found!');
                    return false;
                }
            });
            var username = this.options['username'];
            if(username == null) {
                username = read_cookie('castillo_username');
            }
            $el.find('#message_container').css({"overflow-y": "scroll", "height": "400px"});
            if(username == null) {
                this.display_username_form(this.element, this.options);
            } else {
                this.start_chat(this.element, this.options, username);
            }
        },

        display_username_form: function(el, options) {
            var username = prompt("Please enter your username", null);
            if(username == null) {
                this.display_username_form(el, options);
            }
            this.start_chat(el, options, username);
        },

        start_chat: function(el, options, username) {
            create_cookie('castillo_username', username, 365);
            this.options['username'] = username;
            this.load_room_messages(this.element, this.options);
            this.open_socket(this.element, this.options);
        },

        open_socket: function(el, options) {
            var self = this;
            if(this.options['username'] == null) {
                console.error('To open a socket for chat you need to have a username.');
            }
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            this.socket = new WebSocket(ws_scheme + '://'+window.location.host+'/chat/general');
            this.socket.onmessage = function(message) {
                var data = JSON.parse(message.data);
                self.append_message(el, options, data);
            };
            this.socket.onopen = function(event) {
                self.socket.send(JSON.stringify({
                    "event": "connected",
                    "username": self.options['username']
                }))
            }
            $(el).find('#message_send').on('click', function(event) {
                self.send_message(el, options);
                return false;
            });
        },

        send_message: function(el, options) {
            var message = {
                event: "message",
                message: $(el).find('#message_input').val(),
            }
            this.socket.send(JSON.stringify(message));
            $(el).find('#message_input').val('');
            $(el).find('#message_input').focus();
        },

        append_message: function(el, options, data) {
            var o = this.message_obj.clone();
            o.find(".media-body > p").text(data.message);
            o.find(".media-heading").text(data.username);
            $(el).find('#message_container').append(o);
            $(el).find('#message_container').scrollTop(1E10);
        },

        load_room_messages: function (el, options) {
            var self = this;
            $.get('/api/chat/room/general/?format=json')
                .done(function(json_response) {
                    if(json_response['success']) {
                        $.each(json_response['messages'], function(i) {
                            self.append_message(el, options, this);
                        });
                    }
                });
        }
    };

    // A really lightweight plugin wrapper around the constructor,
    // preventing against multiple instantiations
    $.fn[pluginName] = function (options) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName,
                    new Plugin(this, options));
            }
        });
    };

})(jQuery, window, document);