define(['openlayers', 'crow-layermgmt'], function () {
    var ol = require('openlayers'),
        layerMgmt = require('crow-layermgmt');

    var STYLE,
        STYLE_CACHE,
        openStreetMap;

    var initialise = function() {
        STYLE = new ol.style.Style({
            fill: new ol.style.Fill({
                color: 'rgba(255, 255, 255, 0.6)'
            }),
            stroke: new ol.style.Stroke({
                color: '#319FD3',
                width: 1
            }),
            text: new ol.style.Text({
                font: '12px Calibri,sans-serif',
                fill: new ol.style.Fill({
                    color: '#000'
                }),
                stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 3
                })
            })
        });

        STYLE_CACHE = [STYLE];

        openStreetMap = new ol.layer.Tile({
            source: new ol.source.OSM({
                projection: 'EPSG:3857'
            })
        });
        openStreetMap.set('name', 'Open Street Map');

    }

    var CrowOL = function (mapTarget) {

        this.map = new ol.Map({
            layers: [],
            target: mapTarget,
            view: new ol.View({
                center: [1492977, 6855322],
                zoom: 6
            })
        });

        this.styleCache = [];

        this.layerTree = new layerMgmt.LayerTree(this.map);

        CrowOL.prototype.addStyle = function (style) {
            this.styleCache.push(style);
        };

    };

    return { CrowOL: CrowOL };
});
