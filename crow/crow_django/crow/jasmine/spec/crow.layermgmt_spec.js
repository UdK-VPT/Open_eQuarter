define(['crow-layermgmt', 'openlayers'], function () {

    var ol = require('openlayers'),
    layerMgmt = require('crow-layermgmt');

    describe('Crow Layer-Management Module test - ', function() {

        describe('API - CrowLayerMGMT module', function (){
            it('should load properly using requirejs', function () {
                expect(layerMgmt).toBeDefined();
            });
        });


        describe('Unittest - LayerTree', function () {
            var map,
                LayerTree;

            beforeEach(function() {
                map = new ol.Map({layers: []});
                LayerTree = new layerMgmt.LayerTree();
            });

            it('should add a given layer to the layer-list', function () {
                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                layerList = LayerTree.layers;
                expect(layerList.length).toEqual(1);
                expect(layerList).toContain(layer);
            });
        });

    });
});