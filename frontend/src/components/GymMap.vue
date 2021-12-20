<template>
  <form
    :action="targetUrl"
    method="post"
  >
    <slot name="csrf" />
    <div
      id="popup"
      ref="popup"
      class="ol-popup"
      @keyup.esc="closePopover"
    >
      <a
        id="popup-closer"
        href="#"
        class="ol-popup-closer"
        @click="closePopover"
      />
      <div id="popup-content">
        <p>You clicked here:</p>
        <code>' {{ selectedCoordinate }} </code>
      </div>
      <input
        type="submit"
        value="Submit"
      >
    </div>
    <slot name="management-form" />
    <input
      :id="totalBouldersId"
      type="hidden"
      :name="totalBouldersName"
      :value="totalBoulders"
    >
    <div
      id="map-root"
      ref="map-root"
    />

    <input
      v-for="(coordinates, index) in boulderCoordinates"
      :id="boulderId(index)"
      :key="index"
      :name="boulderName(index)"
      :value="coordinates"
      geom_type="POINT"
      type="text"
    >
  </form>

  <span>this is the gym map for gym {{ gymName }}</span>
</template>

<script>
import {GeoJSON} from 'ol/format';
import Map from 'ol/Map';
import View from 'ol/View';
import {Projection} from 'ol/proj';
import {Image, Vector as VectorLayer} from 'ol/layer';
import {ImageStatic, Vector as VectorSource} from 'ol/source';
import {containsCoordinate, getCenter} from 'ol/extent';
import {Collection, Overlay} from 'ol';
import {Draw} from 'ol/interaction';

import 'ol/ol.css';


export default {
  name: 'GymMap',
  props: {
    gymName: {
      type: String,
      default: 'wrong',
    },
    gymMapProperties: {
      type: Object,
      default: function() {
        return {
          width: 0,
          height: 0,
          path: '',
        };
      },
    },
    prefix: {
      type: String,
      default: 'boulder',
    },
    initialBoulderCoordinates: {
      type: Array,
      default: function() {
        return [];
      },
    },
  },
  data() {
    return {
      jsonFormat: new GeoJSON(),
      selectedCoordinate: 'none yet',
      boulderCoordinates: this.initialBoulderCoordinates,
    };
  },
  computed: {
    totalBoulders() {
      return this.boulderCoordinates.length;
    },
    totalBouldersName() {
      return this.prefix + '-TOTAL_FORMS';
    },
    totalBouldersId() {
      return 'id_' + this.totalBouldersName;
    },
    // Popover showing the position the user clicked
    popover() {
      return new Overlay({
        element: this.$refs['popup'],
        autoPan: true,
        autoPanAnimation: {
          duration: 250,
        },
      });
    },
    featureCollection() {
      const featureCollection = new Collection();
      const self = this;
      // Set handler for serializing newly added and modified features
      featureCollection.on('add', function(event) {
        self.boulderCoordinates.push(
            self.jsonFormat.writeGeometry(event.element.getGeometry()));
        self.popover['feature'] = event.element;
      });
      return featureCollection;
    },
    targetUrl() {
      return `/bouldern/${this.gymName}/map/`;
    },
    extent() {
      return [0, 0, this.gymMapProperties.width, this.gymMapProperties.height];
    },
    projection() {
      return new Projection({
        code: 'xkcd-image',
        units: 'pixels',
        extent: this.extent,
      });
    },
    // Add icon drawing interaction
    drawInteraction() {
      const draw = new Draw({
        type: 'Point',
        source: this.source,
        condition: (event) => containsCoordinate(this.extent, event.coordinate),
      });
      // Set handler for opening popup on draw
      draw.on('drawend', (event) => {
        const coordinate = event.feature.getGeometry().getCoordinates();
        this.selectedCoordinate = coordinate;
        this.popover.setPosition(coordinate);
      });
      return draw;
    },
    source() {
      const source = new VectorSource({
        features: this.featureCollection,
        useSpatialIndex: false, // improves performance
      });
      // Populate with initial features
      this.boulderCoordinates.forEach(
          (coordinates) => source.addFeature(
              this.jsonFormat.readFeature(coordinates)));
      return source;
    },
    map() {
      // Initialize map
      const map = new Map({
        layers: [
          // This layer contains the map image
          new Image({
            source: new ImageStatic({
              url: this.gymMapProperties.path,
              projection: this.projection,
              imageExtent: this.extent,
            }),
          }),
          // This layer is where icons are drawn on
          new VectorLayer({
            source: this.source,
            updateWhileAnimating: true,
            updateWhileInteracting: true,
          }),
        ],
        target: this.$refs['map-root'],
        view: new View({
          projection: this.projection,
          center: getCenter(this.extent),
          zoom: 1,
          maxZoom: 8,
        }),
      });
      map.addOverlay(this.popover);
      map.addInteraction(this.drawInteraction);
      return map;
    },
  },
  mounted() {
    this.map;
  },
  methods: {
    boulderName(index) {
      return `${this.prefix}-${index}-coordinates`;
    },
    boulderId(index) {
      return `id_${this.boulderName(index)}`;
    },
    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
    closePopover() {
      this.featureCollection.remove(this.popover.feature);
      this.popover.setPosition(undefined);
      // todo: figure out if this is necessary
      // this.closer.blur();
      return false;
    },
  },
};
</script>
<!--todo: make sure features are kept and serialized properly-->
<style scoped>
#map-root {
  width: 100%;
  height: 100%;
}
</style>
