define([
    'OpenLayers'
], function(ol){
    String.format = function () {
        // The string containing the format items (e.g. "{0}")
        // will and always has to be the first argument.
        var theString = arguments[0];

        // start with the second argument (i = 1)
        for (var i = 1; i < arguments.length; i++) {
            // "gm" = RegEx options for Global search (more than one instance)
            // and for Multiline search
            var regEx = new RegExp("\\{" + (i - 1) + "\\}", "gm");
            theString = theString.replace(regEx, arguments[i]);
        }

        return theString;
    }

    var layerFromGeoJSON = function (url, STYLE, STYLE_CACHE, name) {
        var json_layer,
            start,
            end;

        json_layer = new ol.layer.Vector({
            source: new ol.source.Vector({
                url: url,
                format: new ol.format.GeoJSON()
            }),
            style: function (feature, resolution) {
                STYLE.getText().setText(resolution < 5000 ? feature.get('name') : '');
                return STYLE_CACHE;
            }
        });

        if (name === undefined) {
            start = url.lastIndexOf('/') + 1;
            end = url.lastIndexOf('.') - start;
            name = url.substr(start, end);
        }
        json_layer.set('name', name);

        return json_layer;
    }

    return {
        layerFromGeoJSON: layerFromGeoJSON
    };
});