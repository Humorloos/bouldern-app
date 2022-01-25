<template>
  <div
    id="popup"
    ref="popup"
    class="ol-popup"
    :style="{visibility: loaded ? 'visible' : 'hidden'}"
  >
    <v-container id="popup-content">
      <v-btn
        id="popup-closer"
        flat
        size="small"
        icon="mdi-close"
        href="#"
        class="ol-popup-closer"
        @click="closePopover"
      />
      <v-row>
        <v-col>
          Difficulty:
          <color-select
            id="id-difficulty-select"
            v-model="selectedDifficulty"
            :color-options="difficultyLevelColors"
            @update:model-value="updateDifficultyLevel($event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          Hold-Color:
          <color-select
            id="id-color-select"
            v-model="selectedColor"
            :color-options="colorOptions"
            @update:model-value="updateHoldColor($event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <vue-form
            :api-path="`/bouldern/gym/${gym.id}/boulder/`"
            :form="{
              coordinates: selectedCoordinates,
              color_id: selectedColor.id,
              difficulty_id: selectedDifficulty.id,
            }"
            @submitted="onSubmitted"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
  <div
    id="map-root"
    ref="map-root"
  />
</template>

<script>
/** @file view with interactive gym map */

import {mapActions, mapMutations, mapState} from 'vuex';
import {Collection, Overlay} from 'ol';
import {Projection} from 'ol/proj';
import {ImageStatic, Vector as VectorSource} from 'ol/source';
import {Draw} from 'ol/interaction';
import {containsCoordinate, getCenter} from 'ol/extent';
import Map from 'ol/Map';
import {Image as ImageLayer, Vector as VectorLayer} from 'ol/layer';
import View from 'ol/View';
import {GeoJSON} from 'ol/format';
import VueForm from '../components/VueForm.vue';
import ColorSelect from '../components/ColorSelect.vue';
import {Circle, Fill, Icon, Stroke, Style} from 'ol/style';

export default {
  name: 'GymMap',
  components: {
    VueForm,
    ColorSelect,
  },
  data() {
    return {
      gym: {
        boulder_set: [{
          coordinates: '',
        }],
        map: '',
        id: 0,
        difficultylevel_set: [{
          id: -1,
          level: 0,
          color: {
            name: '',
            color: '#60522d',
          },
        }],
      },
      colorOptions: [{
        name: '',
        color: '#60522d',
        id: -1,
      }],
      selectedCoordinates: {},
      selectedDifficulty: {
        name: '',
        id: -1,
        color: '#ffffff',
      },
      selectedColor: {
        name: '',
        id: -1,
        color: '#ffffff',
      },
      mapImage: new Image(),
      jsonFormat: new GeoJSON(),
      shadowStyle: new Style({
        image: new Icon({
          src: this.axios.defaults.baseURL +
              'static/bouldern/images/shadow.png',
          scale: 0.5,
          opacity: 0.3,
        }),
      }),
      featureCollection: new Collection(),
      loaded: false,
    };
  },
  computed: {
    ...mapState({
      authToken: 'authToken',
      activeGym: 'activeGym',
    }),
    /**
     * todo
     */
    mapImageSource() {
      return new ImageStatic({
        url: this.gym.map,
        projection: this.projection,
        imageExtent: this.extent,
      });
    },
    /**
     * todo
     */
    imageLayer() {
      // This layer contains the map image
      return new ImageLayer({
        source: this.mapImageSource,
      });
    },
    /**
     * The options for the difficulty level of newly created boulders
     *
     * @returns {{color: *, name: *, id: *}[]} the difficulty level options
     */
    difficultyLevelColors() {
      return this.gym.difficultylevel_set.map(
          ({id, level, color}) => (
            {color: color.color, id: id, name: level + 1}));
    },
    /**
     * Gets the name of the gym to show the map of and sets it as the active gym
     * if a new gym was opened
     *
     * @returns {string} the name of the gym of which to show the map
     */
    gymName() {
      if (this.$route.fullPath === '/') {
        return this.activeGym;
      } else {
        const gymName = this.$route.params.gymName;
        this.setActiveGym(gymName);
        return gymName;
      }
    },
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
     * The map's extent
     *
     * @returns {number[]} the map's extent
     */
    extent() {
      const asdf = this.imageLayer;
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
          this.imageLayer,
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
    this.requestWithJwt({
      method: 'GET',
      apiPath: `/bouldern/gym/?name=${this.gymName}`,
    }).then((response) => {
      this.gym = response.data[0];
      this.mapImage.src = this.gym.map;
      this.mapImage.onload = () => {
        // Populate with initial features
        this.gym.boulder_set.forEach((boulder) => {
          const feature = this.jsonFormat.readFeature(boulder.coordinates);
          // debugger;
          feature.setStyle(this.getBoulderStyle(
              boulder.color.color,
              boulder.difficulty.color.color,
          ));
          this.source.addFeature(feature);
        });
        // Set handler for opening popup on draw
        this.drawInteraction.on('drawend', this.openPopover);
        this.loaded = true;
        this.map;
      };
    });
    this.requestWithJwt({
      method: 'GET',
      apiPath: `/bouldern/color/`,
    }).then((response) => {
      this.colorOptions = response.data;
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
    ...mapMutations({
      setActiveGym: 'setActiveGym',
    }),
    ...mapActions({
      requestWithJwt: 'requestWithJwt',
    }),
    /**
     * todo
     */
    getBoulderStyle(holdColor, difficultyColor) {
      const colorStyle = new Style({
        image: new Circle({
          fill: new Fill({
            color: difficultyColor,
          }),
          stroke: new Stroke({
            color: holdColor,
            width: 6,
            lineDash: [7.4, 8.05],
            lineDashOffset: 3.45,
          }),
          radius: 10,
        }),
      });
      return [colorStyle, this.shadowStyle];
    },
    /**
     * Adjusts the currently selected hold color when selecting a difficulty
     * level todo: add more
     */
    updateDifficultyLevel(event) {
      this.featureCollection.getArray().at(-1)
          .setStyle(this.getBoulderStyle(event.color, event.color));
      this.selectedColor = this.colorOptions.filter(
          (colorOption) => colorOption.color === event.color)[0];
    },
    /**
     * todo
     */
    updateHoldColor(event) {
      this.featureCollection.getArray().at(-1).setStyle(
          this.getBoulderStyle(event.color, this.selectedDifficulty.color));
    },
    /**
     * Removes the popover's feature from the featureCollection and blurs the
     * popover.
     *
     * @returns {boolean} false (don't follow the ref)
     */
    closePopover() {
      this.featureCollection.pop();
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
    openPopover(event) {
      event.feature.setStyle(this.getBoulderStyle(
          this.selectedColor.color, this.selectedDifficulty.color));

      const geometry = event.feature.getGeometry();
      this.selectedCoordinates = this.jsonFormat
          .writeGeometryObject(geometry);

      if (this.popover.getPosition() !== undefined) {
        this.closePopover();
      }
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
  height: 100%;
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
  top: 2px;
  right: 8px;
}
</style>
