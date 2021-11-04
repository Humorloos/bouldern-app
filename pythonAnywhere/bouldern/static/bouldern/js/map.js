'use strict';


// Map views always need a projection.  Here we just want to map image
// coordinates directly to map coordinates, so we create a projection that uses
// the image extent in pixels.
const extent = [0, 0, 1024, 968];
const projection = new ol.proj.Projection({
    code: 'xkcd-image',
    units: 'pixels',
    extent: extent,
});

function MapWidget(options) {
    const map = new ol.Map({
        layers: [
            new ol.layer.Image({
                source: new ol.source.ImageStatic({
                    attributions: '© <a href="https://xkcd.com/license.html">xkcd</a>',
                    url: options.url,
                    projection: projection,
                    imageExtent: extent,
                }),
            }),
        ],
        target: 'map',
        view: new ol.View({
            projection: projection,
            center: ol.extent.getCenter(extent),
            zoom: 2,
            maxZoom: 8,
        }),
    });
}