define(['openlayers'], function() {
    var ol = require('openlayers');

    var LayerTree = function() {
        this.layers = new Array('1');

        LayerTree.prototype.add = function () {

        };
    };

    return { LayerTree: LayerTree };
});