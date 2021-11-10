'use strict';

{
// Map views always need a projection.  Here we just want to map image
// coordinates directly to map coordinates, so we create a projection that uses
// the image extent in pixels.
    const jsonFormat = new ol.format.GeoJSON();

    function MapWidget(options) {
        const projection = options.base_layer.getSource().getProjection();
        const extent = projection.getExtent();
        this.options = options;

        // Initialize map
        this.map = new ol.Map({
            layers: [this.options.base_layer],
            target: options.map_id,
            view: new ol.View({
                projection: projection,
                center: ol.extent.getCenter(extent),
                zoom: 1,
                maxZoom: 8,
            }),
        });

        // Add icon drawing interaction
        this.featureCollection = new ol.Collection();
        const source = new ol.source.Vector({
            features: this.featureCollection,
            useSpatialIndex: false // improves performance
        });
        this.map.addInteraction(
            new ol.interaction.Draw({
                type: "Point",
                source: source,
                condition: event => ol.extent.containsCoordinate(extent, event.coordinate),
            }))

        // This is where icons are drawn on
        this.featureOverlay = new ol.layer.Vector({
            map: this.map,
            source: source,
            updateWhileAnimating: true,
            updateWhileInteracting: true,
        });

        // Set handler for newly added and modified features
        const self = this;
        this.featureCollection.on('add', function (event) {
            const feature = event.element;
            feature.on('change', function () {
                self.serializeFeatures();
            });
            self.serializeFeatures();
        });
    }

    MapWidget.prototype.serializeFeatures = function () {
        const geometry = new ol.geom.MultiPoint(
            this.featureOverlay.getSource().getFeatures().map(feature => feature.getGeometry().getCoordinates()))
        document.getElementById(this.options.id).value = jsonFormat.writeGeometry(geometry);
    };

    window.MapWidget = MapWidget;
}