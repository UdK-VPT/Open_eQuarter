define(['openlayers'], function() {
    var ol = require('openlayers');

    var LayerTree = function() {
        this.layers = new Array();

        LayerTree.prototype.add = function (layer) {
            this.layers.push({
                olLayer: layer,
                name: 'Unnamed'
            })
        };
    };

    return { LayerTree: LayerTree };
});
