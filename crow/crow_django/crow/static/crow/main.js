require.config({
    baseUrl: 'static/crow',
    shim : {
        bootstrap : { deps :['jquery'] }
    },
    paths: {
        jquery: ['//code.jquery.com/jquery-1.11.3.min', 'libs/jquery/jquery.min'],
        bootstrap: ['//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min', 'libs/bootstrap/bootstrap.min'],
        domReady: 'libs/require/domReady'
    },

    global: {
        deps: ['jquery', 'bootstrap']
    }
});

require(['jquery', 'bootstrap', 'js/init']);
