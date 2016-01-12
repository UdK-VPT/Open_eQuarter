define([
    'domReady!',
    'jquery',
    'openlayers',
    'crow-openlayers',
    'crow-googlemaps'
], function(dr, $, ol, CrowOpenlayers, CrowGM){

    var openStreetMap,
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

   var format = new ol.format.WKT();
    var feature = format.readFeature('MULTIPOLYGON (((394044.6499988663708791 5817495.6270224926993251, 394043.2299988652230240 5817493.2910224935039878, 394052.6889988657203503 5817487.8800224959850311, 394055.1029988661175594 5817486.4980224948376417, 394056.1839988652500324 5817485.8800224950537086, 394055.9869988653808832 5817485.5710224946960807, 394048.4979988653794862 5817473.8640224933624268, 394047.5859988664160483 5817474.4250224940478802, 394045.0669988648733124 5817475.8240224914625287, 394030.1939988648518920 5817484.0810224935412407, 394037.1919988655718043 5817495.0590224955230951, 394039.4129988658241928 5817498.5420224964618683, 394044.6499988663708791 5817495.6270224926993251)))');
    feature.getGeometry().transform('EPSG:4326', 'EPSG:3857');
    var vector = new ol.layer.Vector({
        source: new ol.source.Vector({
            features: [feature]
        })
    });
    CrowOL.map.addLayer(vector);


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