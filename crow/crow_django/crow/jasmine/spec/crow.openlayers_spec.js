define(['crow-openlayers', 'openlayers'], function(CrowOpenlayers, ol){

    describe('Crow Openlayers Module test -', function () {

        describe('API - CrowOL module', function () {
            it('should load properly using requirejs', function () {
                expect(CrowOpenlayers).toBeDefined();
            });

            it('has an CrowOL-object', function() {
                expect(CrowOpenlayers.CrowOL).toBeDefined();
            });

            it('should have a constructor function', function () {
                var CrowOL = new CrowOpenlayers.CrowOL('div-id');
                expect(CrowOL).toBeDefined();
            });
        });

        describe('CrowOL - unittest object', function() {
            var CrowOL,
                mapTarget = 'my-div';

            beforeEach(function () {
               CrowOL = new CrowOpenlayers.CrowOL(mapTarget);
            });

            it('should have a map with a target set as passed in the init function', function () {
                var map = CrowOL.map;
                expect(map).toBeDefined();
                expect(map.get('target')).toEqual(mapTarget);
            });

            it('should have a style-cache containing the style passed in the add style function', function () {
               var style = new ol.style.Style({
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
                expect(CrowOL.styleCache).toContain(style);


            });

        });

    }); // Crow Openlayers Module test
});// define