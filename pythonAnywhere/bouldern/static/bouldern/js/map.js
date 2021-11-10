'use strict';


// Map views always need a projection.  Here we just want to map image
// coordinates directly to map coordinates, so we create a projection that uses
// the image extent in pixels.

function MapWidget(options) {
    const projection = options.base_layer.getSource().getProjection();
    const extent = projection.getExtent();
    const source = new ol.source.Vector();
    const map = new ol.Map({
        layers: [
            options.base_layer,
            new ol.layer.Vector({
                source: source
            })
        ],
        target: options.map_id,
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