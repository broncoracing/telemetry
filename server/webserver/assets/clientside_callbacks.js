function binarySearch(array, target) {
    let lo = 0, hi = array.length;
    while (lo < hi) {
        let mi = (lo + hi) >> 1;
        let diff = target - array[mi].number;
        if (diff === 0) return array[mi];
        else if (diff < 0) hi = mi;
        else lo = mi + 1;
    }
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_data_from_websockets: function(new_data, current_data, columns) {
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
                return [current_data, columns];
            } else {
                // Data came out-of-order, find where to insert the new data
                console.log("Data out of order");
                let insert_index = binarySearch(current_data.index, parsed_data.index[0]);
                current_data.index = current_data.index.slice(0, insert_index).concat(parsed_data.index).concat(current_data.index.slice(insert_index));
                current_data.data = current_data.data.slice(0, insert_index).concat(parsed_data.data).concat(current_data.data.slice(insert_index));
                return [current_data, columns];
            }
        },

        update_graph_from_data: function(data, figs) {
//            console.log(figs);
            return figs.map(function(figure){
                if(!figure){
                    return {
                        data:[],
                        layout:{
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
                                title: { text: "int data" }
                            },
                        }
                    };
                }
//                console.log(figure);
                let y_text = figure.layout.yaxis.title.text; // TODO use data name instead
                let data_column_idx = data.columns.findIndex(el => el === y_text);
                if(data_column_idx == -1) {
                    return figure;
                }

                let fig_data = [{
                    x: data.index,
                    y: data.data.map(x => x[data_column_idx])
                }];
                return {'data': fig_data, 'layout': figure.layout}; // For some reason this is needed instead of just returning figure.
            });
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
        update_number_display: function(data, labels, current_value) {
//            console.log(labels);
            output = new Array();
            for(var i = 0; i < labels.length; i++){
                let data_column_idx = data.columns.findIndex(el => el === labels[i]);
                if(data_column_idx < 0){
                    output.push(0)
                }
                let value = data.data[data.data.length-1][data_column_idx];
                let previous_val = (''+current_value[i]).replace('-','');
                previous_length = ('' + previous_val).length;
                new_int_length = ('' + value.toFixed()).length;
                new_length = ('' + value).length;
                if(new_length === new_int_length){
                    output.push(('000000' + value).slice(-(Math.max(new_length, previous_length).toFixed())));
                } else {
                    let min_decimals = 5 - new_int_length;
                    output.push(value.toFixed(Math.max(min_decimals, previous_length - new_int_length - 1)));
                }
            }
            return output;
        },

        update_thermometer_widget: function(data, maxs, mins, labels) {
            output_val = new Array();
            output_max = new Array();
            output_min = new Array();
            for(var i = 0; i < labels.length; i++){
                let data_column_idx = data.columns.findIndex(el => el === labels[i]);
                if(data_column_idx < 0){
                    output_val.push(0);
                    output_max.push(maxs[i]);
                    output_min.push(mins[i]);
                }
                let value = data.data[data.data.length-1][data_column_idx];
                let new_max = Math.max(maxs[i], value);
                let new_min = Math.min(mins[i], value)
                output_val.push(value);
                output_max.push(new_max)
                output_min.push(new_min);
            }
            return [output_val, output_max, output_min];
        },
        update_indicator: function(data, labels) {
//            console.log(labels);
            return labels.map(function(l){
                let data_column_idx = data.columns.findIndex(el => el === l);
                if(data_column_idx < 0){
                    return 0;
                }
                return data.data[data.data.length-1][data_column_idx] > 0;
            });
        },
    }
});
