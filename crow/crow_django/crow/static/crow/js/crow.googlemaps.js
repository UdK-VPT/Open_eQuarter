define(['jquery'], function ($) {

    var lookupAddress;

    lookupAddress = function (addressString) {
        var data,
            url = "http://maps.google.com/maps/api/geocode/json",
            promise;

        data = {
            address: addressString,
            sensor: "false"
        };

        promise = $.get(url, data);

        return promise;
    };

    return {
       lookupAddress: lookupAddress
   };
});