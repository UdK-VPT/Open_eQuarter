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
                expect(layerList[0].olLayer).toEqual(layer);
            });

            it('should name the layer as "Unnamed" if no name was passed when adding the layer', function () {
                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                addedLayer = LayerTree.layers[0];
                expect(addedLayer.name).toEqual('Unnamed');
            });

            it('should add the layers name, if given', function () {
                layer = new ol.layer.Vector();
                name = 'LayerName';
                LayerTree.add(layer, name);
                addedLayer = LayerTree.layers[0];
                expect(addedLayer.name).toEqual(name);
            });
        });

    });
});
