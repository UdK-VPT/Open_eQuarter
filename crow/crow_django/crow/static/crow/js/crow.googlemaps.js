define(['jquery'], function ($) {

    var defaultAddress,
        ajaxPromise,
        lookupAddress;

    defaultAddress = {
        geometry : {
            location: {
                lat: 52.3110,
                lng: 13.2424
            }
        }
    };


    ajaxPromise = function (data) {
        var url,
            response_data;

        url = "http://maps.google.com/maps/api/geocode/json",
        response_data = $.get(url, data);

        return response_data;
    };


    lookupAddress = function (addressString) {
        var addressDict = addressString,
            data = {
                address: addressString,
                sensor: "false"
            },
            promise,
            result;

        promise = ajaxPromise(data);

        return promise.done(function (data){
            result = data.results[0];
            console.log(result);
            addressDict = result;
            return addressDict;

        });
    };

    return {
       lookupAddress: lookupAddress
   };
});