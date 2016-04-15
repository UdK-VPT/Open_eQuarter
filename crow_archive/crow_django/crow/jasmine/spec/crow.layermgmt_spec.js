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
                LayerTree = new layerMgmt.LayerTree(map);
            });

            it('should have access to the ol-map', function () {
                expect(LayerTree.olMap).toEqual(map);
            });

            it('should add a given layer to the layer-list', function () {
                var layer,
                    layerList,
                    addedLayer;

                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                layerList = LayerTree.layers;
                expect(layerList.length).toEqual(1);
                expect(layerList[0].olLayer).toEqual(layer);
            });

            it('should name the layer as "Unnamed" if no name was passed when adding the layer', function () {
                var layer,
                    addedLayer;

                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                addedLayer = LayerTree.layers[0];
                expect(addedLayer.name).toEqual('Unnamed');
            });

            it('should add the layers name, if given', function () {
                var layer,
                    addedLayer;

                layer = new ol.layer.Vector();
                name = 'LayerName';
                LayerTree.add(layer, name);
                addedLayer = LayerTree.layers[0];
                expect(addedLayer.name).toEqual(name);
            });

            it('should add a position argument to the layer', function () {
                var layer,
                    position,
                    addedLayer;

                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                position = 0;
                addedLayer = LayerTree.layers[position];
                expect(addedLayer.position).toEqual(position);
            });

            it('should increment the position properly (starting from zero)', function () {
                var layer,
                    position,
                    addedLayer;

                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                position = 2;
                addedLayer = LayerTree.layers[position];
                expect(addedLayer.position).toEqual(position);
            });

            it('should add the layer to the ol-map as well', function () {
                var layer,
                    olLayerCollection,
                    olLayer,
                    addedLayer;

                layer = new ol.layer.Vector();
                LayerTree.add(layer);
                addedLayer = LayerTree.layers[0].olLayer;
                olLayerCollection = map.getLayers();
                olLayer = olLayerCollection.getArray()[0];
                console.log(map.getLayers());
                expect(olLayer).toEqual(addedLayer);
            });
        });

    });
});
