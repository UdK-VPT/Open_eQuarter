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
            it('should return a dictionary containing the coordinates which correspond to the given address', function (done) {
                var addressPromise,
                    geo_location,
                    lat,
                    lon;

                addressPromise = CrowGM.lookupAddress('Berlin Mitte');
                addressPromise.done(function (data){
                    result = data.results[0];
                    geo_location = result.geometry.location;
                    lat = geo_location.lat;
                    lon = geo_location.lng;
                    expect(lat).toBe(52.5306438);
                    expect(lon).toBe(13.3830683);
                    done();
                });
            });
        });
    });

});