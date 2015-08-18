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

var map = new ol.Map({
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM({projection: 'EPSG:3857'})
    }),
    shapes,
    bldData,
    invArea   
  ],
  target: 'map',
  view: new ol.View({
    center: [1492977,6855322],
    zoom: 6
  })
});



document.getElementById('add-centroids').onclick = function () {
    map.addLayer(data);
};


var wmsBerlinLayer = new ol.layer.Tile({
	source: new ol.source.TileWMS({
		preload: Infinity,
		url: 'http://fbinter.stadt-berlin.de/fb/wms/senstadt/k06_06ewdichte2012',
		serverType:'geoserver',
		params:{
			'LAYERS': "Einwohnerdichte 2012",
            'TILED': true
		}
	})
});


document.getElementById('add-wmslayer').onclick = function () {
    map.addLayer(wmsBerlin);
};

