define(['crow-openlayers'], function(CrowOL){

    describe('Crow Openlayers Module test -', function () {

        describe('API - CrowOL module', function () {
            it('should load properly using requirejs', function () {
                expect(CrowOL).toBeDefined();
            });

            it('has an init-function', function() {
                expect(CrowOL.initialise).toBeDefined();
            });

        });
    });

});