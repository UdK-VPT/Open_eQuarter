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
    var layerStack = $('div.layerStack');
    layersMenu.innerHTML = String.format('<i class="fa fa-list-alt"></i> Layers ({0})', numberOfLayers);
    layerStack.text('');
    
    for (var i = 0; i < numberOfLayers; i++) {
                    layer = layers.item(i);
                    name = layer.get('name')
                    layer.set('id', i);
                    anchor = '<a class="list-group-item" id="{0}">';
                    anchor = String.format(anchor, i);
                    removeBtn = '<button class="btn btn-xs btn-warning pull-left">\
                                    <i class="glyphicon glyphicon-remove"></i></button>'; 
                    span = '<span class="pull-right">';
                    upBtn = '<button class="btn btn-xs btn-warning">\
                                <i class="glyphicon glyphicon-arrow-up"></i></button>';            
                    downBtn = '<button class="btn btn-xs btn-warning">\
                                <i class="glyphicon glyphicon-arrow-down"></i></button>';                    
                    layerBtn = anchor + removeBtn + ' ' + name + span + upBtn + downBtn + '</span></a>';
                    layerStack.prepend(layerBtn);
                    
                    if( layer.getVisible() )
                        $('div.layerStack a:first').addClass('active');
                    $('div.layerStack a:first').unbind('click');
                    $('div.layerStack a:first').click({layerName: name}, function( event ) {
                        layerCtlListener(event, event.data.layerName);
                });
    }   
}

function layerCtlListener( event, layerName ) {
    var classes = event.target.classList;
    if ( classes.contains("list-group-item") ) {
        toggleVisibility(layerName);
    } else if ( classes == "glyphicon glyphicon-arrow-up" ) {
        raiseLayer(layerName);
    } else if ( classes == "glyphicon glyphicon-arrow-down" ) {
        lowerLayer(layerName);
    } else if ( classes.contains("btn-warning") ) {
        target = $( event.target );
        target.children().click();
    } else if ( classes == "glyphicon glyphicon-remove" ) {
        removeLayer(layerName);
    }
}


function toggleVisibility(layerName) {
    var layer = findByName(layerName);
    if (layer !== null) {
        visibility = layer.getVisible();
        if (visibility) {
            layer.setVisible(false);
            $('a#' + layer.get('id')).removeClass('active');
        } else {
           layer.setVisible(true);
            $('a#' + layer.get('id')).addClass('active');
        }
    }
}

function inLayerList( layer, list ) {
    for ( var i = 0; i < list.getLength(); i++ ) {
        if ( layer === list.item(i) ) 
            return i;
    }
    return -1;
}

function raiseLayer(layerName) {
    var layer = findByName(layerName);
    var layers = map.getLayers();
    var index = inLayerList(layer, layers);
    
    if ( index >= 0 && index < layers.getLength() - 1 ) {
        former = layers.removeAt(index);
        layers.insertAt(index + 1, former);
    }
}

function lowerLayer(layerName) {
    var layer = findByName(layerName);
    var layers = map.getLayers();
    var index = inLayerList(layer, layers);

    if ( index > 0 ) {
        former = layers.removeAt(index);
        layers.insertAt(index - 1, former);
    }
}

function removeLayer(layerName) {
    var layer = findByName(layerName);
    var layers = map.getLayers();
    layers.remove(layer);
}

var limitProperties = function() {
    doc_height = $(document).height();
    max = doc_height - $('#properties').offset().top - doc_height * 0.05;
    $('#properties').css('max-height', max);
}

$(document).ready(limitProperties);
$(window).resize(limitProperties);