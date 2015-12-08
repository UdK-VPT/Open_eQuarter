define([
    'domReady!',
    'jquery',
    'openlayers',
    'crow-openlayers',
    'crow-googlemaps'
], function(dr, $, ol, CrowOpenlayers, CrowGM){

    var CrowOL,
        openStreetMap,
        style;

    CrowOL = new CrowOpenlayers.CrowOL('map');
    openStreetMap = new ol.layer.Tile({
        source: new ol.source.OSM({
            projection: 'EPSG:3857'
        })
    });
    openStreetMap.set('name', 'Open Street Map');

    style = new ol.style.Style({
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

    CrowOL.addStyle(style);
    CrowOL.map.addLayer(openStreetMap);

    $('#addressLookup').on('submit', function (event) {
        event.preventDefault();
        var addressField,
            address,
            promisedResult;

        addressField = $('#addressLookup input:first:text');
        address = addressField.val();
        promisedResult = CrowGM.lookupAddress(address);

        promisedResult.done(function (data){
            var result,
                geo_location,
                lat,
                lon,
                extent,
                map;
            if(data && data.results[0]) {
                result = data.results[0];
                geo_location = result.geometry.location;
                lat = geo_location.lat;
                lon = geo_location.lng;

                addressField.css('color', 'rgb(0, 0, 0)');
                extent = [lon - 0.02, lat - 0.02, lon + 0.02, lat + 0.02];
                extent = ol.extent.applyTransform(extent, ol.proj.getTransform("EPSG:4326", "EPSG:3857"));
                map = CrowOL.map;
                map.getView().fit(extent, map.getSize());
            } else {
                addressField.css('color', 'rgb(255, 0, 0)');
            }
        });

    });

});