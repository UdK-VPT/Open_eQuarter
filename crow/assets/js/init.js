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

var shapes = layerFromGeoJSON('../layers/BLD_Shapes.geojson');
var bldData = layerFromGeoJSON('../layers/BLD_Data.geojson');
var invArea = layerFromGeoJSON('../layers/Investigation Area.geojson')

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

// Add a listener to the 'Open layer...'-file dialog
$(document).on('change', '.btn-file :file', function() {
  var files,
      reader;

  files = $(this).get(0).files; // FileList object

  // Loop through the FileList and render image files as thumbnails.
  for (var i = 0, file; file = files[i]; i++) {

    // Only process image files.
    if (!file.name.match('geojson$')) {
      continue;
    }

    reader = new FileReader();

    // Closure to capture the file information.
    reader.onload = (function(theFile) {
      return function(e) {
        // Render layer
        var layer,
            url = e.target.result,
            name,
            end;

        name = escape(theFile.name);
        end = name.lastIndexOf('.');
        name = name.substr(0, end);
        layer = layerFromGeoJSON(url, name);
        map.addLayer(layer);
      };
    })(file);

    // Read in the image file as a data URL.
    reader.readAsDataURL(file);
  }
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


var HIGHLIGHTSTYLE_CACHE = {};
var CLICKSTYLE_CACHE = {};

var featureOverlay = new ol.layer.Vector({
  source: new ol.source.Vector(),
  map: map,
  style: function(feature, resolution) {
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
  map: map,
  style: function(feature, resolution) {
    var text = resolution < 5000 ? feature.get('name') : '';
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
            color: '#000'
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
