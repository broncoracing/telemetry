/**
 * Return 0 <= i <= array.length such that !pred(array[i - 1]) && pred(array[i]).
 */
 function binarySearch(array, target) {
    let lo = -1, hi = array.length;
    while (1 + lo < hi) {
        const mi = lo + ((hi - lo) >> 1);
        if (array[mi] > target) {
            hi = mi;
        } else {
            lo = mi;
        }
    }
    return hi;
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_data_from_websockets: function(new_data, current_data, columns) {
            const MAX_DATA_POINTS = 100;
//            console.log(columns);
            // Parse data from the received string
            let parsed_data = JSON.parse(new_data);
//            console.log(current_data);

            // No new data, keep current data.
            if(!parsed_data || !parsed_data.hasOwnProperty('index') || parsed_data.index.length == 0){
                console.log('New data empty, keeping current');
                return [current_data, columns];
            }

            parsed_data.index = parsed_data.index.map(t => new Date(t));

            // No current data, just use new data
            if(!current_data || !current_data.hasOwnProperty('index') || current_data.index.length == 0){
                console.log('Current data undefined/empty, using new data instead');
                return [parsed_data, parsed_data.columns];
            }

            // Ensure the columns are the same
            // TODO: Make this not just dump the old data, but insert columns of empty data to match it
            if(!parsed_data.columns.every((value, index) => value === current_data.columns[index])){
                console.log("Columns changed! Discarding old data.");
                console.log(parsed_data.columns, current_data.columns);
                return [parsed_data, parsed_data.columns];
            }

            if(parsed_data.index[0] > current_data.index[current_data.index.length - 1]){
                // Data came in-order, append to the end of the data list(s).
                current_data.data = current_data.data.concat(parsed_data.data);
                current_data.index = current_data.index.concat(parsed_data.index);
            } else {
                // Data came out-of-order, find where to insert the new data
                console.log("Data out of order");
                let insert_index = binarySearch(current_data.index, parsed_data.index[0]);
                current_data.index = current_data.index.slice(0, insert_index).concat(parsed_data.index).concat(current_data.index.slice(insert_index));
                current_data.data = current_data.data.slice(0, insert_index).concat(parsed_data.data).concat(current_data.data.slice(insert_index));
            }

            if(current_data.length > MAX_DATA_POINTS){
                current_data = current_data.slice(current_data.length - MAX_DATA_POINTS);
            }

            return [current_data, columns];
        },

        update_graph_from_data: function(data, settings, fig){// title, axes, persistence, max_points, line_style, ) {
            var title = '';
            var axes = undefined;
            var persistence = 30;
            var max_points = 2000;
            var line_style = 'line';
            // Ensure the settings are set up properly
            if(['title', 'axes', 'persistence', 'max_points', 'line_style'].every(attr => settings.hasOwnProperty(attr))){
                title = settings.title;
                axes = settings.axes;
                persistence = settings.persistence;
                max_points = settings.max_points;
                line_style = settings.line_style;
            }

            let fig_layout = {
                title:title,
                autosize:true,
                margin: { t: 30 },
                xaxis: {
                    anchor: "x",
                    autorange: true,
                    tickformatstops: [
                        {
                            "dtickrange": [null, 59999],
                            "value": "%H:%M:%S s"
                        },
                        {
                            "dtickrange": [59999, null],
                            "value": "%H:%M m"
                        }
                    ],
                    title: { text: "time" }
                },
                yaxis: {
                    anchor: "y",
                    autorange: true,
                    // title: { text: "int data" }
                },
            };
            
            if(!axes){
                return {'data': [], 'layout': fig_layout};
            }

            let oldest_allowed = data.index[data.index.length - 1] - persistence * 1000.0;
            let oldest_data_pt = Math.max(binarySearch(data.index, oldest_allowed), data.index.length - max_points);
           
            console.log(data.index.length);
            console.log(oldest_data_pt);
           
            let fig_data = axes.map(
                    axis => data.columns.findIndex(el => el === axis)
                ).filter(idx => idx >= 0)
                .map(function(idx){
                return {
                    type: 'scattergl',
                    x: data.index.slice(oldest_data_pt),
                    y: data.data.slice(oldest_data_pt).map(x => x[idx]),
                    mode: line_style,
                    name: data.columns[idx]
                }});


            return {'data': fig_data, 'layout': fig_layout};
        },

        update_number_widget: function(data, labels) {
//            console.log(labels);
            return labels.map(function(l){
                let data_column_idx = data.columns.findIndex(el => el === l);
                if(data_column_idx < 0){
                    return 0;
                }
                return data.data[data.data.length-1][data_column_idx];
            });
        },
        update_number_display: function(data, settings, current_value) {
            if(!settings.hasOwnProperty('value')){
                return [0, 'No source'];
            }
            let data_column_idx = data.columns.findIndex(el => el === settings.value);
            if(data_column_idx < 0){
                return [0, 'No source'];
            }else{
                let value = data.data[data.data.length-1][data_column_idx];
                let previous_val = (''+current_value).replace('-','');
                previous_length = ('' + previous_val).length;
                new_int_length = ('' + value.toFixed()).length;
                new_length = ('' + value).length;
                if(new_length === new_int_length){
                    return [('000000' + value).slice(-(Math.max(new_length, previous_length).toFixed())), settings.value];
                } else {
                    let min_decimals = 5 - new_int_length;
                    return [value.toFixed(Math.max(min_decimals, previous_length - new_int_length - 1)), settings.value];
                }
            }
        },

        update_thermometer_widget: function(data, settings) {
            // Ensure the settings are set up properly
            if(!['value', 'min', 'max'].every(attr => settings.hasOwnProperty(attr))){
                return [0, 10, 0, 'No data'];
            }

            let label = settings.value;
            let data_column_idx = data.columns.findIndex(el => el === label);
            if(data_column_idx < 0){
                return [0, settings.max, settings.min, 'No data'];
            }

            let value = data.data[data.data.length-1][data_column_idx];
            let new_max = Math.max(settings.max, value);
            let new_min = Math.min(settings.min, value);

            return [value, new_max, new_min, settings.value];
        },
        update_indicator: function(data, settings) {

            if(!settings.hasOwnProperty('value')){
                return [false, 'No source'];
            }
            let data_column_idx = data.columns.findIndex(el => el === settings.value);
            if(data_column_idx < 0){
                return [false, 'No source'];
            }
            return [data.data[data.data.length-1][data_column_idx] > 0, settings.value];
        },
    }
});
