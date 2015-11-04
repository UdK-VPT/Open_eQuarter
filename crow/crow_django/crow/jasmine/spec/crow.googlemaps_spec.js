define(['crow-googlemaps'], function(CrowGM) {

    describe('Crow Googlemaps Module test -', function () {

        describe('API - CrowGM module', function () {
            it('should load porperly using requirejs', function () {
                expect(CrowGM).toBeDefined();
            });

            it('should have a lookupAddress-method, which accepts one parameter', function () {
                expect(CrowGM.lookupAddress).toBeDefined();
            });
        });

        describe('Unittest - CrowGM', function () {
            it('should return a dictionary containing the coordinates which correspond to the given address', function () {
                var address,
                    geo_location,
                    lat,
                    lon;

                address = CrowGM.lookupAddress('Berlin Mitte');
                geo_location = address.geometry.location;
                lat = geo_location.lat;
                lon = geo_location.lng;
                expect(lat).toBe(52.3110);
                expect(lon).toBe(13.2424);
            });
        });
    });

});