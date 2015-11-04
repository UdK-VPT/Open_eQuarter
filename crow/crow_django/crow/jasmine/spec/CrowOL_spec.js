describe('CrowOL API test - CrowOL Module', function() {
    var CrowOL;

    // Use require.js to fetch the module
    it("should load the AMD module", function(done) {
        require(['js/CrowOL'], function (loadedModule) {
            CrowOL = loadedModule;
            done();
        });
    });

    it('was loaded properly', function () {
       expect(CrowOL).toBeDefined();
    });

    it('has an init-function', function() {
        expect(CrowOL.initialise()).toBeDefined();
    });
});