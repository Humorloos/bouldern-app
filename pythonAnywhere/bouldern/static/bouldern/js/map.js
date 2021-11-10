'use strict';


// Map views always need a projection.  Here we just want to map image
// coordinates directly to map coordinates, so we create a projection that uses
// the image extent in pixels.

function MapWidget(options) {
    const extent = [0, 0, options.map_width, options.map_height];
    const projection = new ol.proj.Projection({
        code: 'xkcd-image',
        units: 'pixels',
        extent: extent,
    });
    const source = new ol.source.Vector();
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
            new ol.layer.Vector({
                source: source
            })
        ],
        target: 'map',
        view: new ol.View({
            projection: projection,
            center: ol.extent.getCenter(extent),
            zoom: 1,
            maxZoom: 8,
        }),
    });
    map.addInteraction(
        new ol.interaction.Draw({
            type: "Point",
            source: source,
            condition: event => ol.extent.containsCoordinate(extent, event.coordinate),
        }))
}