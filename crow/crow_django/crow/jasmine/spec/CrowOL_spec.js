describe('Test CrowOL', function() {
  var crowOlModule;

  // Use require.js to fetch the module
  it("should load the AMD module", function(done) {
    require(['js/CrowOL'], function (loadedModule) {
      crowOlModule = loadedModule;
      done();
    });
  });

  //run tests that use the crowOlModule object
  it("can access the AMD module", function() {
    expect(crowOlModule.speak()).toBe("hello");
  });
});