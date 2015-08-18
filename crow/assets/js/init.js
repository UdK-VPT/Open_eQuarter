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
    //map.addLayer(invArea);
    updateLayerList();
    map.getLayers().on('add', updateLayerList);
}


var highlightStyleCache = {};

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
            width: 3
          })
        })
      })];
    }
    return highlightStyleCache[text];
  }
});

var highlight;
var displayFeatureInfo = function(pixel) {

  var feature = map.forEachFeatureAtPixel(pixel, function(feature, layer) {
    return feature;
  });

    var propertiesSheet = document.getElementById('dataSheet');
    if (feature) {

        propertiesSheet.innerHTML = 'BLD_ID:' + feature.get('BLD_ID') + '<br>' +
                                    'AREA: ' + feature.get('AREA') + '<br>' +
                                    'PERIMETER: ' + feature.get('PERIMETER');
    } else {
        propertiesSheet.innerHTML = '&nbsp;';
    }

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
  var pixel = map.getEventPixel(evt.originalEvent);
  displayFeatureInfo(pixel);
});

map.on('click', function(evt) {
  displayFeatureInfo(evt.pixel);
});