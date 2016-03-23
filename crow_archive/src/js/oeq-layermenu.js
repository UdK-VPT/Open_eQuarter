define([
    'jquery',     // lib/jquery/jquery
    'OpenLayers' // lib/underscore/underscore
], function($, ol){
    function updateLayerList(MAP) {

        var layers = MAP.getLayers();
        var numberOfLayers = layers.getLength();
        var layersMenu = document.getElementById("layersMenu");
        var layerStack = $('#layerStack');
        layersMenu.innerHTML = String.format('<i class="fa fa-list-alt"></i> Layers ({0})', numberOfLayers);
        layerStack.text('');

        for (var i = 0; i < numberOfLayers; i++) {
            var layer = layers.item(i);
            var name = layer.get('name')
            layer.set('id', i);
            var anchor = '<a class="list-group-item" id="{0}">';
            anchor = String.format(anchor, i);
            var removeBtn = '<button class="btn btn-xs btn-warning pull-left">\
                                        <i class="glyphicon glyphicon-remove"></i></button>';
            var span = '<span class="pull-right">';
            var upBtn = '<button class="btn btn-xs btn-warning">\
                                    <i class="glyphicon glyphicon-arrow-up"></i></button>';
            var downBtn = '<button class="btn btn-xs btn-warning">\
                                    <i class="glyphicon glyphicon-arrow-down"></i></button>';
            var layerBtn = anchor + removeBtn + ' ' + name + span + upBtn + downBtn + '</span></a>';
            layerStack.prepend(layerBtn);

            if (layer.getVisible())
                $('#layerStack a:first').addClass('active');
            $('#layerStack a:first').unbind('click');
            $('#layerStack a:first').click({
                layerName: name
            }, function (event) {
                layerCtlListener(event, event.data.layerName);
            });
        }
    }

    function layerCtlListener(event, layerName) {
        var classes = event.target.classList;
        if (classes.contains("list-group-item")) {
            toggleVisibility(layerName);
        } else if (classes == "glyphicon glyphicon-arrow-up") {
            raiseLayer(layerName);
        } else if (classes == "glyphicon glyphicon-arrow-down") {
            lowerLayer(layerName);
        } else if (classes.contains("btn-warning")) {
            target = $(event.target);
            target.children().click();
        } else if (classes == "glyphicon glyphicon-remove") {
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

    function inLayerList(layer, list)  {
        for (var i = 0; i < list.getLength(); i++) {
            if (layer === list.item(i))
                return i;
        }
        return -1;
    }

    function raiseLayer(layerName) {
        var layer = findByName(layerName);
        var layers = MAP.getLayers();
        var index = inLayerList(layer, layers);

        if (index >= 0 && index < layers.getLength() - 1) {
            former = layers.removeAt(index);
            layers.insertAt(index + 1, former);
        }
    }

    function lowerLayer(layerName) {
        var layer = findByName(layerName);
        var layers = MAP.getLayers();
        var index = inLayerList(layer, layers);

        if (index > 0) {
            former = layers.removeAt(index);
            layers.insertAt(index - 1, former);
        }
    }

    function removeLayer(layerName) {
        var layer = findByName(layerName);
        var layers = MAP.getLayers();
        layers.remove(layer);
    }

    /**
     * Finds a layers given a 'name' attribute.
     * @param {type} name
     * @returns {unresolved}
     */
    function findByName(name) {
        var layers = MAP.getLayers();
        var length = layers.getLength();
        for (var i = 0; i < length; i++) {
            if (name === layers.item(i).get('name')) {
                return layers.item(i);
            }
        }
        return null;
    }

    var limitProperties = function () {
        var doc_height = $(document).height();
        var max = doc_height - $('#properties').offset().top - doc_height * 0.05;
        $('#properties').css('max-height', max);
    }

    $(document).ready(limitProperties);
    $(window).resize(limitProperties);

    // Copied (except for map manipulation)
    function lookupAddress() {
        var address = $('#addressLookup input:first').val();
        $.ajax({
            type: "GET",
            url: "http://maps.google.com/maps/api/geocode/json",
            dataType: "json",
            data: {
                address: address,
                sensor: "false"
            },
            success: function (data) {
                if (data && data.results[0]) {
                    $('#addressLookup input:first:text').css('color', 'rgb(0, 0, 0)');
                    var addr = data.results[0];
                    $('#addressLookup input:first').val('');
                    var geo_loc = addr.geometry.location;
                    var lat = geo_loc.lat;
                    var lon = geo_loc.lng;
                    var extent = [lon - 0.02, lat - 0.02, lon + 0.02, lat + 0.02];
                    extent = ol.extent.applyTransform(extent, ol.proj.getTransform("EPSG:4326", "EPSG:3857"));
                    MAP.getView().fit(extent, MAP.getSize());
                } else {
                    $('#addressLookup input:first:text').css('color', 'rgb(255, 0, 0)');
                }
            },
            error: function () {
                alert("Error.");
            }
        });
    }

    // Add a listener to the 'Open layer...'-file dialog
    $(document).on('change', '.btn-file :file', function () {
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
            reader.onload = (function (theFile) {
                return function (e) {
                    // Render layer
                    var layer,
                        url = e.target.result,
                        name,
                        end;

                    name = escape(theFile.name);
                    end = name.lastIndexOf('.');
                    name = name.substr(0, end);
                    layer = layerFromGeoJSON(url, name);
                    MAP.addLayer(layer);
                };
            })(file);

            // Read in the image file as a data URL.
            reader.readAsDataURL(file);
        }
    });

    return {
        update: updateLayerList
    }
});