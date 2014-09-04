/**
 * Zircon Datasocket
 *
 * Javascript API for communicating with a Zircon Datastore.
 */
ZirconDatasocket = function() {

    function ZirconDatasocket(on_connect, on_disconnect) {

        // Websocket connection to server
        this.socket = io.connect('/data', {resource: 'zircon'});

        // When connected
        this.socket.on('connect', function() {
            console.log('ZirconDatasocket connected.');
            if(on_connect) on_connect();
        });

        // When disconnected
        this.socket.on('disconnect', function() {
           console.warn('ZirconDatasocket disconnected!');
            if(on_disconnect) on_disconnect();
        });

        // Print debugs?
        this.debug_mode = true;
    }

    ZirconDatasocket.prototype.emit_raw = function(channel, msg, callback) {

        if(this.debug_mode)
            console.log('SENT: [' + channel + '] ' + JSON.stringify(msg));

        this.socket.emit(channel, msg, callback);
    };

    ZirconDatasocket.prototype.emit = function(channel, msg, callback) {
        var self = this;
        this.emit_raw(channel, msg, function(reply) {
            if(self.debug_mode)
                console.log('RECV: [' + channel + '] ' + JSON.stringify(reply));
            if(callback) callback(reply);
        });
    };

    ZirconDatasocket.prototype.debug = function(msg) {
        var self = this;
        if(!self.debug_mode) return;
        self.emit('debug', msg);
    };

    ZirconDatasocket.prototype.time = function(callback) {
        this.emit('time', {}, callback);
    };

    ZirconDatasocket.prototype.list_signals = function(callback) {
        this.emit('list_signals', {}, callback);
    };

    ZirconDatasocket.prototype.get_database_name = function(arg, callback) {
        if(!arg) arg = {};
        this.emit('get_database_name', arg, callback);
    };

    ZirconDatasocket.prototype.get_timeseries = function(arg, callback) {
        if(!arg) arg = {};
        this.emit('get_timeseries', arg, callback);
    };

    ZirconDatasocket.prototype.get_last_points = function(arg, callback) {
        if(!arg) arg = {};
        this.emit('get_last_points', arg, callback);
    };

    return ZirconDatasocket;
}();
