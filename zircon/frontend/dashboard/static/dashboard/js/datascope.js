/**
 *
 */

/**
 * Object that holds information about one signal in a DataScope
 */
function DataSeries(signal_id) {

    // Signal ID
    this.name = signal_id;

    // Buffer of data received from the server
    this.data_buffer = [];

    // Current index inside the data buffer
    this.data_inx = 0;

    // Dictionary for an NVD3 series
    this.data = {

        // Name to show in the legend
        key: this.name,

        // Current set of values being plotted
        values: []
    };

    // Last data point that was plotted, used to make sure
    // we don't double plot with a new buffer
    this.last_time_plotted = 0;
}

/**
 * Methods for DataSeries class
 */
DataSeries.prototype = {

    constructor: DataSeries,

    /**
     * Update the plotted data to include only points within
     * the current time window.
     */
    update_dataset: function (time, time_window) {

        // Unplot data past the time window
        for(var i = this.data.values.length - 1; i >= 0; i--) {
            if(this.data.values[i]['x'] < time - time_window) {
                this.data.values.splice(0, i+1);
                break;
            }
        }

        // If reached the end of the buffer, return
        if(this.data_inx >= this.data_buffer.length) {
            //console.warn('Signal ' + this.name + ' reached end of buffer!');
            return;
        }

        // Plot new data until current time
        while (this.data_buffer[this.data_inx][0] < time) {

            var point = this.data_buffer[this.data_inx];

            if ((this.data.values.length == 0) ||
                (point[0] > this.data.values[this.data.values.length - 1]['x'])) {

                // Make sure we don't replot points
                if(point[0] > this.last_time_plotted) {
                    this.data.values.push({
                        x: point[0],
                        y: point[1]
                    });
                    this.last_time_plotted = point[0];
                }
            }
            this.data_inx += 1;

            if(this.data_inx >= this.data_buffer.length) return;
        }

    },

    /**
     * New data received from server, update the buffer.
     */
    update_data_buffer: function (data) {

        var timeseries = $.map(data, function(row) {
            return [[row[0]/1000, row[1]]];
        }).reverse();

        this.data_buffer = timeseries;
        this.data_inx = 0;
    },

    get_url_encoding: function () {
        return this.name;
    }
};

// ---------------------------------------------------------------------------

function DataScope (scope_id, start_time) {

    this.id = scope_id;

    this.start_time = start_time;

    // Time window being shown (ms)
    this.time_window = 10000;

    // Canonical time variable of the app.
    this.time = this.start_time;

    this.started = false;

    this.paused = false;

    this.nvdata = [];

    // NVD3 chart object
    this.chart = undefined;

    // List of DataSeries in this DataScope
    this.series = {};

    // Optional Y domain. If undefined, autoscales
    this.y_domain = undefined;

    this.svg = undefined;

    // render template
    var source = $("#data-scope-template").html();
    var template = Handlebars.compile(source);
    $('.scopes_row').append(template({
        scope_id: this.id,
        signal_ids: signal_ids,
    }));

    var self = this;

    this.container = $('#scope-container-' + this.id);

    this.container.find('.add-signal-modal select.selectpicker').selectpicker({});

    // Focus on the signal id field when the add signal
    // model opens, for quickness of input
    this.container.find('.add-signal-button').click(function() {
        window.setTimeout(function () {
            self.container.find('div.signal-select button').focus();
        }, 300);
    });

    this.container.find('.confirm-add-signal-button').click(function() {

        var signal_id = self.container.find('.signal-select').next().
            children('button').children('span.filter-option').text();

        self.add_series(signal_id);
        self.update();

        update_url();

        self.container.find('.add-signal-modal').modal('hide');
    });

    this.container.find('.confirm-remove-scope-button').click(function() {
        self.container.find('.add-signal-modal').modal('hide');
        delete_scope(self.id);
    });

    this.container.find('.set-range-button').click(function() {
        self.container.find('.error-text').hide();
    });

    this.container.find('.confirm-set-range-button').click(function() {

        var y_min_str = self.container.find('.y-min-field').val();
        var y_max_str = self.container.find('.y-max-field').val();

        var y_min = parseFloat(y_min_str);
        var y_max = parseFloat(y_max_str);

        var valid = true;

        if(isNaN(y_min)) {

            if(!y_min_str) {
                y_min = undefined;
            } else {
                valid = false;
            }
        }

        if(isNaN(y_max)) {

            if(!y_max_str) {
                y_max = undefined;
            } else {
                valid = false;
            }
        }

        if(valid) {
            self.set_y_domain(y_min, y_max);
            self.container.find('.set-range-modal').modal('hide');
        } else {
            self.container.find('.error-text').show();
        }
    });

    this.container.find('.remove-signal-button').click(function() {
        var select = self.container.find('select.remove-signal-select');

        console.log(self.series);
        select.empty();
        for(var serie_name in self.series) {
            select.append('<option>' + serie_name + '</option>');
        }
        select.selectpicker('refresh');
    });

    this.container.find('.confirm-remove-signal-button').click(function() {

        self.container.find('.remove-signal-modal').modal('hide');

        var serie_name = self.container.find('select.remove-signal-select').next().
            children('button').children('span.filter-option').text();

        self.remove_series(serie_name);
    });

    this.init();
}


DataScope.prototype = {

    constructor: DataScope,

    new_data: function (data) {

        for(var signal_name in data) {
            if(signal_name in this.series) {
                this.series[signal_name].update_data_buffer(data[signal_name])
            }
        }
    },

    pause: function() {
        this.paused = true;
    },

    resume: function() {
        this.paused = false;
    },

    set_y_domain: function(y_min, y_max) {
        this.y_domain = [y_min, y_max];
        this.chart.forceY(this.y_domain);
        this.update();
    },

    clear_y_domain: function() {
        this.y_domain = undefined;
        this.chart.forceY([]);
        this.update();
    },

    tick: function (time) {

        if(this.paused) return;

        this.time = time;

        // Add data points
        for(var series_name in this.series) {
            this.series[series_name].update_dataset(
                this.time,
                this.time_window
            )
        }

        if(!this.chart) {
            console.warn('chart undefined!');
            return;
        }

        this.chart.forceX([this.time - this.time_window, this.time]);
        this.update();

    },

    init: function () {

        this.started = true;

        // Proxy for this
        var self = this;

        nv.addGraph(function() {
            var chart = nv.models.lineChart()
            //.margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
            .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
            .transitionDuration(0)  //how fast do you want the lines to transition?
            .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
            .showYAxis(true)        //Show the y-axis
            .showXAxis(true)        //Show the x-axis
            //.interpolate("basis")
            .rightAlignYAxis(false)
            ;

            chart.xAxis     //Chart x-axis settings
                .axisLabel('Time (ms)')
                .tickFormat(function(d) {
                    var label = (d - self.start_time)/1000;
                    if(label < 0) return '';
                    return d3.format('.3f')(label);
                    //return new Date(label).toString('mm:ss dd-MM-yyyy');//d3.format('0.2f')(label);
                });

            chart.yAxis     //Chart y-axis settings
                .axisLabel('Value')
                .tickFormat(d3.format('.03f'));

            self.svg = d3.select('#scope-container-' + self.id + ' .nvd3-container')
                .append('svg'); //Select the <svg> element you want to render the chart in.

            self.svg.datum(self.nvdata)         //Populate the <svg> element with chart data...
                .call(chart);          //Finally, render the chart!

            // Update the chart when window resizes
            nv.utils.windowResize(function() { self.update() });

            self.chart = chart;
            return chart;
        });

    },

    add_series: function (signal_id) {
        this.add_series_obj(new DataSeries(signal_id));
    },

    add_series_obj: function (dataseries) {
        this.series[dataseries.name] = dataseries;
        this.nvdata.push(dataseries.data);
    },

    remove_series: function (serie_name) {

        delete this.series[serie_name];

        var remove_inx = -1;
        for(var i = 0; i < this.nvdata.length; i++) {
            var d = this.nvdata[i];
            if(d['key'] == serie_name)
                remove_inx = i;
        }

        if(remove_inx >= 0)
            this.nvdata.splice(remove_inx, 1);

        this.update();
        update_url();
    },

    update: function() {

        this.chart.update();
    },

    get_url_encoding: function() {
        var self = this;
        return this.id + '=' + $.map(Object.keys(this.series), function(serie_name) {
            return self.series[serie_name].get_url_encoding();
        }).join(',');
    },
};
