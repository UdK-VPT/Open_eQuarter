var STYLE = new ol.style.Style({
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
var STYLE_CACHE = [STYLE];

var shapes = layerFromGeoJSON('layers/BLD_Shapes.geojson');

var openStreetMap = new ol.layer.Tile({
    source: new ol.source.OSM({
        projection: 'EPSG:3857'
    })
});
openStreetMap.set('name', 'Open Street Map');

var MAP = new ol.Map({
    layers: [openStreetMap],
    target: 'map',
    view: new ol.View({
        center: [1492977, 6855322],
        zoom: 6
    })
});

function oeq_init() {

    MAP.addLayer(shapes);
    updateLayerList();
    MAP.getLayers().on('change', updateLayerList);
    MAP.getLayers().on('add', updateLayerList);
    MAP.getLayers().on('remove', updateLayerList);
}


var HIGHLIGHTSTYLE_CACHE = {};
var CLICKSTYLE_CACHE = {};

var featureOverlay = new ol.layer.Vector({
    source: new ol.source.Vector(),
    map: MAP,
    style: function (feature, resolution) {
        var text = resolution < 5000 ? feature.get('name') : '';
        if (!HIGHLIGHTSTYLE_CACHE[text]) {
            HIGHLIGHTSTYLE_CACHE[text] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#f00',
                    width: 1
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(255,0,0,0.3)'
                }),
                text: new ol.style.Text({
                    font: '12px Calibri,sans-serif',
                    text: text,
                    fill: new ol.style.Fill({
                        color: '#000'
                    }),
                    stroke: new ol.style.Stroke({
                        color: '#f00',
                        width: 3
                    })
                })
            })];
        }
        return HIGHLIGHTSTYLE_CACHE[text];
    }
});
var featureClick = new ol.layer.Vector({
    source: new ol.source.Vector(),
    map: MAP,
    style: function (feature, resolution) {
        var text = resolution < 4 ? feature.get('AREA').toFixed(2) + ' qm' : '';
        if (!CLICKSTYLE_CACHE[text]) {
            CLICKSTYLE_CACHE[text] = [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#f00',
                    width: 1
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(255,0,0,0.1)'
                }),
                text: new ol.style.Text({
                    font: '12px Calibri,sans-serif',
                    text: text,
                    fill: new ol.style.Fill({
                        color: '#fff'
                    }),
                    stroke: new ol.style.Stroke({
                        color: '#f00',
                        width: 4
                    })
                })
            })];
        }
        return CLICKSTYLE_CACHE[text];
    }
});
var clickedFeature;

var highlight;
var displayFeatureInfo = function (feature) {
    limitProperties();
    propertiesSheet = document.getElementById('dataSheet');
    var table = '<style type="text/css">.propSheet {border-collapse: separate; overflow: auto; border-spacing: 2px 0;}' +
        '.propSheet td, .propSheet th { padding: 0 5px; } ' +
        '</style>' +
        '<table class="propSheet">' +
        '<tr><th>Property</th><th>Value</th></tr>';
    var keys = feature.getKeys();
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        table += '<tr><td>' + key + '</td><td>' + feature.get(key) + '</td></tr>';
    }
    table += '</table>';
    propertiesSheet.innerHTML = table;
};
var highlightFeature = function (feature) {
    if (feature !== highlight) {
        if (highlight) {
            featureOverlay.getSource().removeFeature(highlight);
        }
        if (feature) {
            featureOverlay.getSource().addFeature(feature);
        }
        highlight = feature;
    }
};

MAP.on('pointermove', function (evt) {
    if (evt.dragging) {
        return;
    }
    pixel = MAP.getEventPixel(evt.originalEvent);
    feature = MAP.forEachFeatureAtPixel(pixel, function (feature, layer) {
        return feature;
    });
    if (feature) {
        displayFeatureInfo(feature);
        highlightFeature(feature);
    } else if (clickedFeature) {
        displayFeatureInfo(clickedFeature);
        highlightFeature(feature);
    } else {
        highlightFeature(feature);
        propertiesSheet = document.getElementById('dataSheet');
        propertiesSheet.innerHTML = '<p>Click a feature to display its properties.</p>';
    }
});

MAP.on('click', function (evt) {
    pixel = evt.pixel;
    feature = MAP.forEachFeatureAtPixel(pixel, function (feature, layer) {
        return feature;
    });
    if (feature) {
        if (clickedFeature)
            featureClick.getSource().removeFeature(clickedFeature);
        clickedFeature = feature;
        displayFeatureInfo(feature);
        featureClick.getSource().addFeature(feature);
    } else {
        if (clickedFeature)
            featureClick.getSource().removeFeature(clickedFeature);
        clickedFeature = null;
        propertiesSheet = document.getElementById('dataSheet');
        propertiesSheet.innerHTML = '<p>Click a feature to display its properties.</p>';
    }
});