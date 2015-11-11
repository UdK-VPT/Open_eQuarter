define(['jquery'], function ($) {

    var ajaxPromise,
        lookupAddress;

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

        promise = ajaxPromise(data);

        return promise;
    };

    return {
       lookupAddress: lookupAddress
   };
});