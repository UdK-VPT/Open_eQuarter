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
    
    var layerList = document.getElementById("layerList");
    finalList = ""
    
    for ( var i=0; i < numberOfLayers; i++ ) {
        var layer = layers.item(i);
        finalList += "<a href='#' class='list-group-item'><i class='fa fa-globe'></i> " + layer.get('name') + "</a>";
    }
    
    layerList.innerHTML = finalList;
}
