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
                    layer.set('id', i)
                    anchor = '<a class="list-group-item active" \
                            id="{0}" \
                            onclick="toggleVisibility(\'{1}\');" >';
                    anchor = String.format(anchor, i, name);
                    removeBtn = '<button class="btn btn-xs btn-warning pull-left">\
                                    <i class="glyphicon glyphicon-remove"></i></button>'; 
                    span = '<span class="pull-right">';
                    upBtn = '<button class="btn btn-xs btn-warning">\
                                <i class="glyphicon glyphicon-arrow-up"></i></button>';            
                    downBtn = '<button class="btn btn-xs btn-warning">\
                                        <i class="glyphicon glyphicon-arrow-down"></i></button>';
                    layerBtn = anchor + removeBtn + ' ' + name + span + upBtn + downBtn + '</span></a>';
                    layerStack.prepend(layerBtn);
    }
}

/**
 * Finds a layers given a 'name' attribute.
 * @param {type} name
 * @returns {unresolved}
 */
function findByName(name) {
    var layers = map.getLayers();
    var length = layers.getLength();
    for (var i = 0; i < length; i++) {
        if (name === layers.item(i).get('name')) {
            return layers.item(i);
        }
    }
    return null;
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

/**
 * Initialize the stack control with the layers in the map.
 */
function initializeStack() {
    var layers = map.getLayers();
    var length = layers.getLength(), l;
    for (var i = 0; i < length; i++) {
        l = layers.item(i);
        $('div.layerStack').prepend('<li data-layerid="' + l.get('name') + '">' + l.get('name') + '</li>');
    }

    // Change style when select a layer
    $('ul.layerstack li').on('click', function() {
        $('ul.layerstack li').removeClass('selected');
        $(this).addClass('selected');
    });
}

/**
 * Returns the index of the layer within the collection.
 * @param {type} layers
 * @param {type} layer
 * @returns {Number}
 */
function indexOf(layers, layer) {
    var length = layers.getLength();
    for (var i = 0; i < length; i++) {
        if (layer === layers.item(i)) {
            return i;
        }
    }
    return -1;
}


/**
 * Raise a layer one place.
 * @param {type} layer
 * @returns {undefined}
 */
function raiseLayer(layer) {
    var layers = map.getLayers();
    var index = indexOf(layers, layer);
    if (index < layers.getLength() - 1) {
        var next = layers.item(index + 1);
        layers.setAt(index + 1, layer);
        layers.setAt(index, next);

        // Moves li element up
        var elem = $('ul.layerstack li[data-layerid="' + layer.get('name') + '"]');
        elem.prev().before(elem);
    }
}

/**
 * Lowers a layer once place.
 * @param {type} layer
 * @returns {undefined}
 */
function lowerLayer(layer) {
    var layers = map.getLayers();
    var index = indexOf(layers, layer);
    if (index > 0) {
        var prev = layers.item(index - 1);
        layers.setAt(index - 1, layer);
        layers.setAt(index, prev);

        // Moves li element down
        var elem = $('ul.layerstack li[data-layerid="' + layer.get('name') + '"]');
        elem.next().after(elem);
    }
}

$(document).ready(function() {

    initializeStack();

    $('#raise').on('click', function() {
        var layerid = $('ul.layerstack li.selected').data('layerid');
        if (layerid) {
            var layer = findByName(layerid);
            raiseLayer(layer);
        }
    });

    $('#lower').on('click', function() {
        var layerid = $('ul.layerstack li.selected').data('layerid');
        if (layerid) {
            var layer = findByName(layerid);
            lowerLayer(layer);
        }
    });
});