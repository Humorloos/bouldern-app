<template>
  <div
    id="popup"
    ref="popup"
    class="ol-popup"
    :style="{visibility: loaded ? 'visible' : 'hidden'}"
    @keyup.esc="closePopover"
  >
    <!--      shape="round"-->
    <ion-button
      id="popup-closer"
      fill="clear"
      size="small"
      class="ol-popup-closer"
      @click="closePopover"
    >
      <ion-icon
        icon-only
        :icon="close"
      />
    </ion-button>
    <div id="popup-content">
      <p>You clicked here:</p>
      <code>' {{ createdBoulder.coordinates }} </code>
    </div>
    <vue-form
      :api-path="`/bouldern/gym/${mapData.id}/boulder/`"
      :form="createdBoulder"
      @submitted="onSubmitted"
    />
  </div>
  <div
    id="map-root"
    ref="map-root"
  />
</template>

<script>
/** @file view with interactive gym map */

import {mapState} from 'vuex';
import {Collection, Overlay} from 'ol';
import {Projection} from 'ol/proj';
import {ImageStatic, Vector as VectorSource} from 'ol/source';
import {Draw} from 'ol/interaction';
import {containsCoordinate, getCenter} from 'ol/extent';
import Map from 'ol/Map';
import {Image as ImageLayer, Vector as VectorLayer} from 'ol/layer';
import View from 'ol/View';
import {GeoJSON} from 'ol/format';
import {IonIcon, IonButton} from '@ionic/vue';
import {close} from 'ionicons/icons';
import VueForm from '@/components/VueForm';

export default {
  // todo: remove view from name
  name: 'GymMap',
  components: {
    VueForm,
    IonIcon,
    IonButton,
  },
  setup() {
    return {close};
  },
  data() {
    return {
      mapData: {
        boulder_set: [{
          coordinates: '',
        }],
        map: '',
        id: 0,
      },
      createdBoulder: {coordinates: {}},
      mapImage: new Image(),
      jsonFormat: new GeoJSON(),
      loaded: false,
      featureCollection: new Collection(),
    };
  },
  computed: {
    ...mapState([
      'authToken',
    ]),
    /**
     * Popover showing the position the user clicked
     *
     * @returns {Overlay} the popover
     */
    popover() {
      return new Overlay({
        element: this.$refs['popup'],
        autoPan: true,
        autoPanAnimation: {
          duration: 250,
        },
      });
    },
    /**
     * OpenLayers feature collection containing the geographic features in the
     * map
     *
     * @returns {Collection} the feature collection
     */
    featureCollection() {
      return new Collection();
    },
    /**
     * The map's extent
     *
     * @returns {number[]} the map's extent
     */
    extent() {
      return [0, 0, this.mapImage.width, this.mapImage.height];
    },
    /**
     * Projecton from image coordinates to geo-coordinates
     *
     * @returns {Projection} the projection
     */
    projection() {
      return new Projection({
        code: 'xkcd-image',
        units: 'pixels',
        extent: this.extent,
      });
    },
    /**
     * Vector source to draw boulders on
     *
     * @returns {VectorSource} the vector source
     */
    source() {
      return new VectorSource({
        features: this.featureCollection,
        useSpatialIndex: false, // improves performance
      });
    },
    /**
     * Icon drawing interaction for drawing boulder icons. Only allows drawing
     * on the image, not outside of it.
     *
     * @returns {Draw} the draw interaction
     */
    drawInteraction() {
      return new Draw({
        type: 'Point',
        source: this.source,
        condition: (event) => containsCoordinate(this.extent, event.coordinate),
      });
    },
    /**
     * Initializes the gym map with image layer, vector layer, popover, and
     * draw interaction
     *
     * @returns {Map} the gym map
     */
    map() {
      // Initialize map
      const map = new Map({
        layers: [
          // This layer contains the map image
          new ImageLayer({
            source: new ImageStatic({
              url: this.mapData.map,
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
  /**
   * Gets the gym data including the map image's url, saves it and loads the map
   * once the image has loaded
   */
  created() {
    this.axios.get(`/bouldern/gym/?name=${this.$route.params.gymName}`, {
      headers: {
        'authorization': `Bearer ${this.authToken.token}`,
      },
    }).then((response) => {
      this.mapData = response.data[0];
      this.mapImage.src = this.mapData.map;
      this.mapImage.onload = () => {
        // Populate with initial features
        this.mapData.boulder_set.forEach(
            (boulder) => this.source.addFeature(
                this.jsonFormat.readFeature(boulder.coordinates)));
        // Set handler for associating created boulders to popover
        this.featureCollection.on('add',
            (event) => this.popover.feature = event.element);
        // Set handler for opening popup on draw
        this.drawInteraction.on('drawend', this.createBoulder);
        this.loaded = true;
        this.map;
      };
    });
  },
  /**
   * Makes the component available to cypress in test runs
   */
  mounted() {
    if (window.Cypress) {
      window[this.$options.name] = this;
    }
  },
  methods: {
    /**
     * Removes the popover's feature from the featureCollection and blurs the
     * popover.
     *
     * @returns {boolean} false (don't follow the ref)
     */
    closePopover() {
      this.featureCollection.remove(this.popover.feature);
      this.popover.setPosition(undefined);
      return false;
    },
    /**
     * Blurs the popover
     */
    onSubmitted() {
      this.popover.setPosition(undefined);
    },
    /**
     * Handler for draw interaction. Sets created boulder as GeoJSON object and
     * sets the position of the popover to the created boulder
     *
     * @param event the add feature event
     */
    createBoulder(event) {
      const geometry = event.feature.getGeometry();
      this.createdBoulder.coordinates = this.jsonFormat
          .writeGeometryObject(geometry);

      const coordinate = geometry.getCoordinates();
      this.popover.setPosition(coordinate);
    },
  },
};
</script>

<style>
@import '../../node_modules/ol/ol.css';

#map-root {
  width: 100%;
  height: 99%;
}

.ol-popup {
  position: absolute;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #cccccc;
  bottom: 12px;
  left: -50px;
  min-width: 280px;
}

.ol-popup:after, .ol-popup:before {
  top: 100%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}

.ol-popup:after {
  border-top-color: white;
  border-width: 10px;
  left: 48px;
  margin-left: -10px;
}

.ol-popup:before {
  border-top-color: #cccccc;
  border-width: 11px;
  left: 48px;
  margin-left: -11px;
}

.ol-popup-closer {
  text-decoration: none;
  position: absolute;
  top: 4px;
  right: 8px;
}

</style>
