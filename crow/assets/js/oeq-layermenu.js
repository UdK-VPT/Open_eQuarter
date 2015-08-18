document.getElementById('add-centroids').onclick = function () {
    map.addLayer(bldCentroids);
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

function updateLayerList () {
    
    var layers = map.getLayers();
    var numberOfLayers = layers.getLength();
    var layersMenu = document.getElementById("layersMenu");
    layersMenu.innerHTML = "<i class='fa fa-list-alt'></i> Layers (" + numberOfLayers + ")";
    
    for (var i = 0; i < numberOfLayers; i++) {
                    layer = layers.item(i);
                    $('div.layerStack').prepend(
                        '<a class="list-group-item active">'+
                        '<button class="btn btn-xs btn-warning pull-left">'+
                            '<i class="glyphicon glyphicon-remove"> </i></button>' +
                        layer.get('name') +
                        '<span class="pull-right">' +
                        '<button class="btn btn-xs btn-warning">'+
                            '<i class="glyphicon glyphicon-arrow-up"></i></button>' +
                        '<button class="btn btn-xs btn-warning">' +
                            '<i class="glyphicon glyphicon-arrow-down"></i></button>' +
                        '</span>'+
                        '</a>');
                }
}
