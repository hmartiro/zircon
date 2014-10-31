/**
 *
 */

$(function() {

    var scopes = {};

    var zd = new ZirconDatasocket(init, uninit);

    // Whether to print out all sent and received messages
    zd.debug_mode = true;

    // Time difference between client and server
    var t_offset = undefined;

    // How often to request data (ms)
    var data_frametime = 100;

    // How often to update the view (ms)
    var view_frametime = 50;

    // Sample rate of requested timeseries (ms)
    var dt = 100;

    var start_time_server = undefined;

    var paused = false;

    var data_timer_id = null;
    var view_timer_id = null;

    var query_time = 0;

    var data_frametime_real = 0;
    var data_frametime_ref = 0;

    var view_frametime_real = 0;
    var view_frametime_ref = 0;

    function get_time() {
        return Date.now() + t_offset;
    }
    window.get_time = get_time;

    function init() {
        zd.time(function(t) {

            var start_time_client = Date.now();
            start_time_server = Math.round(t/1000);

            t_offset = start_time_server - start_time_client;

            console.log('client: ' + start_time_client +
                ' server: ' + start_time_server + ' offset: ' + t_offset);

            // Create scopes and signals from URL encoding
            load_scopes_from_url(start_time_server);

            data_frametime_ref = Date.now();
            view_frametime_ref = Date.now();

            data_timer_id = setInterval(request_data, data_frametime);
            view_timer_id = setInterval(view_update, view_frametime);

            request_data();
        });
    }

    function uninit() {
        if(data_timer_id) clearInterval(data_timer_id);
        if(view_timer_id) clearInterval(view_timer_id);
    }

    function load_scopes_from_url(t) {

        var url = window.location.search.substr(1);

        var scopedata = url.split('&');
        for(var i = 0; i < scopedata.length; i++) {

            if(scopedata[i] == "") continue;

            var sp = scopedata[i].split('=');

            var scope_id = sp[0];

            // Ignore repeated scope ids
            if(scopes[scope_id]) return;

            var scope = new DataScope(scope_id, t);

            var signals = sp[1].split(',');
            for(var j = 0; j < signals.length; j++) {

                var signaldata = signals[j];

                if(signaldata == "") continue;

                scope.add_series(signaldata);
            }
            scopes[scope.id] = scope;
        }
    }

    function request_data() {

        if(paused) return;

        var series = get_series();

        query_time = Date.now();

        if(!series.length) return;

        var request = {
            signals: series,
            t0: (get_time() - data_frametime * 3) * 1e3,
            t1: (get_time() + 1000) * 1e3,
            dt: dt * 1e3,
            aggregate: 'last',
            limit: 200
        };

        zd.get_timeseries(request, data_update);
    }

    function data_update(data) {

        var now = Date.now();

        query_time = now - query_time;

        data_frametime_real = now - data_frametime_ref;
        data_frametime_ref = now;

        console.log('[Data update] frametime: ' + data_frametime_real +
            ' ms, time: ' + get_time() + ' query_time: ' + query_time);

        for(var scope_name in scopes) {
            scopes[scope_name].new_data(data);
        }
    }

    function view_update() {

        view_frametime_real = Date.now() - view_frametime_ref;
        view_frametime_ref = Date.now();

        //console.log('[View update] frametime: ' + view_frametime_real + ' ms, time: ' + get_time());

        for(var scope_name in scopes) {
            scopes[scope_name].tick(get_time());
        }
    }

    $('.pause-all-button').click(function() {
        paused = true;
        for(var scope_id in scopes)
            scopes[scope_id].pause()
            $('.pause-all-button').hide();
            $('.resume-all-button').show();
    });

    $('.resume-all-button').click(function() {
        paused = false;
        for(var scope_id in scopes)
            scopes[scope_id].resume()
            $('.pause-all-button').show();
            $('.resume-all-button').hide();
    }).hide();

    $('.confirm-add-scope-button').click(function() {

        var scope_field = $('#add-scope-field');
        var scope_id = scope_field.val();
        if(scopes[scope_id]) {
            console.error('Repeated scope id ' + scope_id + ', not adding!');
            return;
        }

        $('.add-scope-modal').modal('hide');
        scope_field.val('');
        scopes[scope_id] = new DataScope(scope_id, start_time_server);
        update_url();
    });

    function get_series() {
        return $.map(scopes, function(scope) {
            return $.map(scope.series, function(s) {
                return s.name;
            });
        });
    }

    window.zd = zd;
    window.scopes = scopes;
});

function get_url_encoding() {

    return '?' + $.map(scopes, function(scope, i) {
        return scope.get_url_encoding();
    }).join('&');
}

function update_url() {
    window.history.pushState({}, '', get_url_encoding());
}

function delete_scope(scope_id) {

    var scope = scopes[scope_id];
    scope.container.remove();
    $('.modal-backdrop').remove();
    scope.pause();

    delete scopes[scope_id];

    update_url();
}
