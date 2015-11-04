require.config({

    shim : {
        bootstrap : { deps :['jquery'] }
    },
    paths: {
        jquery: ['//code.jquery.com/jquery-1.11.3.min', 'libs/jquery/jquery.min'],
        bootstrap: ['//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min', 'libs/bootstrap/bootstrap.min'],
        openlayers: ['//cdnjs.cloudflare.com/ajax/libs/ol3/3.9.0/ol.min', 'libs/openlayers/ol'],
        domReady: 'libs/require/domReady'
    },

    global: {
        deps: ['jquery', 'bootstrap']
    }
});

require(['jquery', 'bootstrap', 'js/init']);
