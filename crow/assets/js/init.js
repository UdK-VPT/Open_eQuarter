var style = new ol.style.Style({
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
var styleCache = [style];

var shapes = new ol.layer.Vector({
    source: new ol.source.Vector({
        url: '../layers/BLD_Shapes.geojson',
        format: new ol.format.GeoJSON()
    }),
    style: function(feature, resolution) {
        style.getText().setText(resolution < 5000 ? feature.get('name') : '');
        return styleCache
    }
});
shapes.set('name', 'BLD_Shapes');
    
var bldData = new ol.layer.Vector({
    source: new ol.source.Vector({
        url: '../layers/BLD_Data.geojson',
        format: new ol.format.GeoJSON()
    }),
    style: function(feature, resolution) {
        style.getText().setText(resolution < 5000 ? feature.get('name') : '');
        return styleCache
    }
});
bldData.set('name', 'BLD_Data');

var invArea = new ol.layer.Vector({
    source: new ol.source.Vector({
        url: '../layers/Investigation Area.geojson',
        format: new ol.format.GeoJSON()
    }),
    style: function(feature, resolution) {
        style.getText().setText(resolution < 5000 ? feature.get('name') : '');
        return styleCache
    }
});
invArea.set('name', 'Investigation Area');

var bldCentroids = new ol.layer.Vector({
    source: new ol.source.Vector({
        url: '../layers/BLD_Centroids.geojson',
        format: new ol.format.GeoJSON()
    }),
    style: function(feature, resolution) {
        style.getText().setText(resolution < 5000 ? feature.get('name') : '');
        return styleCache
    }
});
bldCentroids.set('name', 'BLD_Centroids');

var openStreetMap = new ol.layer.Tile({
  source: new ol.source.OSM({projection: 'EPSG:3857'})
});
openStreetMap.set('name', 'Open Street Map');

var map = new ol.Map({
  layers: [openStreetMap],
  target: 'map',
  view: new ol.View({
    center: [1492977,6855322],
    zoom: 6
  })
});

function oeq_init () {

    map.addLayer(shapes);
    map.addLayer(bldData);
    //map.addLayer(invArea);
    updateLayerList();
    map.getLayers().on('change', updateLayerList);
    map.getLayers().on('add', updateLayerList);
    map.getLayers().on('remove', updateLayerList);
}


var highlightStyleCache = {};
var clickStyleCache = {};

var featureOverlay = new ol.layer.Vector({
  source: new ol.source.Vector(),
  map: map,
  style: function(feature, resolution) {
    var text = resolution < 5000 ? feature.get('name') : '';
    if (!highlightStyleCache[text]) {
      highlightStyleCache[text] = [new ol.style.Style({
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
    return highlightStyleCache[text];
  }
});
var featureClick = new ol.layer.Vector({
  source: new ol.source.Vector(),
  map: map,
  style: function(feature, resolution) {
    var text = resolution < 5000 ? feature.get('name') : '';
    if (!clickStyleCache[text]) {
      clickStyleCache[text] = [new ol.style.Style({
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
            color: '#000'
          }),
          stroke: new ol.style.Stroke({
            color: '#f00',
            width: 4
          })
        })
      })];
    }
    return clickStyleCache[text];
  }
});
var clickedFeature;

var highlight;
var displayFeatureInfo = function(feature) {
    limitProperties();
    propertiesSheet = document.getElementById('dataSheet');
    var table = '<style type="text/css">.propSheet {border-collapse: separate; overflow: auto; border-spacing: 2px 0;}'+
                '.propSheet td, .propSheet th { padding: 0 5px; } '+
                '</style>'+
                '<table class="propSheet">'+
                '<tr><th>Property</th><th>Value</th></tr>';        
    var keys = feature.getKeys();
    for (var i=0; i < keys.length; i++){
        var key = keys[i];
        table += '<tr><td>' + key + '</td><td>' + feature.get(key) + '</td></tr>';
    }
    table += '</table>';
    propertiesSheet.innerHTML = table;
};
var highlightFeature = function(feature) {
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

map.on('pointermove', function(evt) {
    if (evt.dragging) {
        return;
    }
    pixel = map.getEventPixel(evt.originalEvent);
    feature = map.forEachFeatureAtPixel(pixel, function(feature, layer) {
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

map.on('click', function(evt) {
    pixel = evt.pixel;
    feature = map.forEachFeatureAtPixel(pixel, function(feature, layer) {
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