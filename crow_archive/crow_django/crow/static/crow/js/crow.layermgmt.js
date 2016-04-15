define(['openlayers'], function() {
    var ol = require('openlayers');

    var LayerTree = function(map) {
        this.olMap = map;
        this.layers = new Array();

        LayerTree.prototype.add = function (in_layer, in_name) {
            if ( typeof(in_name) === 'undefined' ){
                in_name = 'Unnamed';
            };

            // add a new layer-object to the layer-list
            this.layers.push({
                olLayer: in_layer,
                name: in_name,
                position: this.layers.length
            });

            // add the given layer to the map
            this.olMap.addLayer(in_layer);
        };
    };

    return { LayerTree: LayerTree };
});
