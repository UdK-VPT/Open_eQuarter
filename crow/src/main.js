require.config({
    baseUrl: 'src',
    paths: {
        OpenLayers: 'libs/openlayers/ol',
        jquery: 'libs/jquery/jquery.min',
        bootstrap: '//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js',
        domReady: 'libs/require/domReady'
    },

    global: {
        deps: ['jquery']
    }
});

require(['js/init']);