require.config({
    baseUrl: '/static/crow',

    paths: {
        // libraries
        'jquery': ['//code.jquery.com/jquery-1.11.3.min', 'libs/jquery/jquery.min'],
        'bootstrap': ['//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min', 'libs/bootstrap/bootstrap.min'],
        'openlayers': ['//cdnjs.cloudflare.com/ajax/libs/ol3/3.9.0/ol.min', 'libs/openlayers/ol'],
        'domReady': 'libs/require/domReady',

        // testing
        'jasmine': 'libs/jasmine/jasmine',
        'jasmine-html': 'libs/jasmine/jasmine-html',
        'jasmine-boot': 'libs/jasmine/boot',

        // local modules
        'crow-openlayers': 'js/crow.openlayers',
        'crow-googlemaps': 'js/crow.googlemaps'
    },

    shim : {
        'bootstrap' : {
            deps: ['jquery']
        },
        'jasmine-html': {
            deps: ['jasmine']
        },
        'jasmine-boot': {
            deps: ['jasmine', 'jasmine-html']
        }
    },

    global: {
        deps: ['jquery', 'bootstrap']
    }
});