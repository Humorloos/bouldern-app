<template>
  <div
    id="popup"
    ref="popup"
    class="ol-popup"
    :style="{visibility: loaded ? 'visible' : 'hidden'}"
  >
    <v-btn
      id="popup-closer"
      flat
      size="small"
      icon="mdi-close"
      class="ol-popup-closer"
      @click="closePopover"
    />
    <v-container
      v-if="creating"
      id="popup-content"
    >
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
    <v-container v-else>
      <v-row>
        <v-col>
          <v-btn
            id="retire-boulder"
            flat
            @click="retireBoulder"
          >
            <div>retire</div>
            <br>
            <v-icon>mdi-package-down</v-icon>
          </v-btn>
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

const defaultColor = {
  name: '',
  id: -1,
  color: '#ffffff',
};

export default {
  name: 'GymMap',
  components: {
    VueForm,
    ColorSelect,
  },
  data() {
    return {
      gym: {
        map: '',
        id: 0,
        difficultylevel_set: [{
          id: -1,
          level: 0,
          color: defaultColor,
        }],
      },
      boulders: [{
        coordinates: '',
      }],
      colorOptions: [defaultColor],
      selectedCoordinates: {},
      selectedDifficulty: defaultColor,
      selectedColor: defaultColor,
      mapImage: new Image(),
      jsonFormat: new GeoJSON(),
      shadowStyle: new Style({
        image: new Icon({
          src: this.axios.defaults.baseURL +
              'static/bouldern/images/shadow.png',
          scale: 0.34,
          opacity: 0.6,
        }),
      }),
      extent: [0, 0, 0, 0],
      featureCollection: new Collection(),
      loaded: false,
      creating: false,
      selectedFeature: undefined,
    };
  },
  computed: {
    ...mapState({
      authToken: 'authToken',
      activeGym: 'activeGym',
    }),
    /**
     * The openlayers gym map image source to be used in the image layer.
     *
     * @returns {ImageStatic} the map image source.
     */
    mapImageSource() {
      return new ImageStatic({
        url: this.gym.map,
        projection: this.projection,
        imageExtent: this.extent,
        imageLoadFunction: this.setMapImage,
      });
    },
    /**
     * This layer contains the map image
     *
     * @returns {ImageLayer} the map image layer
     */
    imageLayer() {
      return new ImageLayer({
        className: 'image-layer',
        source: this.mapImageSource,
      });
    },
    /**
     * This layer is where icons are drawn on
     *
     * @returns {VectorLayer} the vector layer
     */
    vectorLayer() {
      return new VectorLayer({
        className: 'vector-layer',
        source: this.vectorSource,
        updateWhileAnimating: true,
        updateWhileInteracting: true,
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
      if (this.$route.matched.some(({name}) => name === 'gymMap')) {
        const gymName = this.$route.params.gymName;
        this.setActiveGym(gymName);
        return gymName;
      } else {
        return this.activeGym;
      }
    },
    /**
     * Popover for creating or editing boulders
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
    vectorSource() {
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
      const drawInteraction = new Draw({
        type: 'Point',
        source: this.vectorSource,
        style: new Style({}),
        condition: (event) => {
          return containsCoordinate(this.extent, event.coordinate) &&
              !this.hasBoulderAtPixel(event.pixel);
        },
      });
      drawInteraction.on('drawend', this.openPopover);
      return drawInteraction;
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
        target: this.$refs['map-root'],
      });
      map.addOverlay(this.popover);
      map.on('pointermove', (event) => {
        const pixel = map.getEventPixel(event.originalEvent);
        const hit = this.hasBoulderAtPixel(pixel);
        map.getTarget().style.cursor = hit ? 'pointer' : '';
      });
      map.on('click', (event) => {
        const feature = map
            .forEachFeatureAtPixel(event.pixel, (feature) => feature);
        if (feature) this.openPopover(feature);
      });
      return map;
    },
  },
  watch: {
    /**
     * Loads new gym map when gym name changes
     */
    gymName() {
      this.featureCollection.clear();
      this.selectedDifficulty = defaultColor;
      this.selectedColor = defaultColor;
      if (this.popover.getPosition()) this.closePopover();
      this.loadGymMap();
    },
  },
  /**
   * Gets the gym data including the map image's url, saves it and loads the map
   * once the image has loaded
   */
  created() {
    this.loadGymMap(this.onGymMapLoaded);
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
    hasBoulderAtPixel(pixel) {
      return this.map.hasFeatureAtPixel(pixel, {
        layerFilter: (layer) => layer
            .getClassName() === this.vectorLayer.getClassName(),
      });
    },
    /**
     * Gets the gym data from the API, loads the gym map image, and deserializes
     * the gym's boulders into the feature collection
     */
    loadGymMap(onLoaded) {
      this.requestWithJwt({
        method: 'GET',
        apiPath: `/bouldern/gym/?name=${this.gymName}`,
      }).then((response) => {
        this.gym = response.data[0];
        this.mapImage.src = this.gym.map;
        this.mapImage.onload = () => {
          this.extent = [0, 0, this.mapImage.width, this.mapImage.height];
          this.map.setLayers([
            this.imageLayer,
            this.vectorLayer,
          ]);
          this.map.setView(new View({
            projection: this.projection,
            center: getCenter(this.extent),
            zoom: 1,
            maxZoom: 8,
          }));
          this.map.removeInteraction(this.drawInteraction);
          this.map.addInteraction(this.drawInteraction);
          if (onLoaded) onLoaded();
        };
        this.requestWithJwt({
          method: 'GET',
          apiPath: `/bouldern/gym/${this.gym.id}/boulder/?is_active=true`,
        }).then((response) => {
          this.boulders = response.data;
          // Populate with initial features
          this.boulders.forEach((boulder) => {
            const feature = this.jsonFormat.readFeature(boulder.coordinates);
            feature.id = boulder.id;
            feature.setStyle(this.getBoulderStyle(
                boulder.color.color,
                boulder.difficulty.color.color,
            ));
            this.vectorSource.addFeature(feature);
          });
        });
      });
    },
    /**
     * Sets the loaded flag and initializes the
     * map
     */
    onGymMapLoaded() {
      this.loaded = true;
      this.map;
    },
    /**
     * Assigns the map image to the provided image. The purpose of this method
     * is to avoid loading the map image twice by assigning the already loaded
     * image instead.
     *
     * @param image image object of map image source.
     */
    setMapImage(image) {
      image.setImage(this.mapImage);
    },
    /**
     * Generates the openlayers style for a boulder with the given hold and
     * difficulty color. The style is a cirle with four small border segments
     * where the cirle is colored in the boulder's difficulty color and the
     * border segments are colored in the boulder's hold color. Behind this
     * style there is another style that serves as the icon's shadow.
     *
     * @param holdColor the boulder's hold color
     * @param difficultyColor the boulder's difficulty color
     * @returns {Style[]} the boulder's style consisting of the two-colored icon
     * and a shadow
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
      return [this.shadowStyle, colorStyle];
    },
    /**
     * Adjusts the currently selected hold color when selecting a difficulty
     * level and Updates both the hold and difficulty color of the most recently
     * added boulder to the provided event's color
     */
    updateDifficultyLevel(event) {
      this.selectedFeature
          .setStyle(this.getBoulderStyle(event.color, event.color));
      this.selectedColor = this.colorOptions.filter(
          (colorOption) => colorOption.color === event.color)[0];
    },
    /**
     * Updates the hold color of the most recently added boulder to the provided
     * event's color
     *
     * @param event a color select update event
     */
    updateHoldColor(event) {
      this.selectedFeature.setStyle(
          this.getBoulderStyle(event.color, this.selectedDifficulty.color));
    },
    /**
     * If in create mode, removes the popover's feature from the
     * featureCollection and (always) blurs the popover.
     */
    closePopover() {
      if (this.creating) this.featureCollection.pop();
      this.popover.setPosition(undefined);
    },
    /**
     *
     */
    retireBoulder() {
      this.requestWithJwt({
        apiPath: `/bouldern/gym/${this.gym.id}/boulder/` +
            `${this.selectedFeature.id}/`,
        method: 'PATCH',
        data: {'is_active': false},
      }).then((response) => {
        console.log(response);
      });
      this.featureCollection.remove(this.selectedFeature);
      this.closePopover();
    },
    /**
     * Blurs the popover
     */
    onSubmitted(response) {
      this.selectedFeature.id = response.data.id;
      this.popover.setPosition(undefined);
    },
    /**
     * Opens the create / edit popover and closes the old one if still open. If
     * called with draw event sets selected coordinates to the event's feature's
     * coordinates and sets the drawn feature's style to the selected colors.
     *
     * @param event the draw event or the clicked feature
     */
    openPopover(event) {
      if (this.popover.getPosition() !== undefined) {
        this.closePopover();
      }

      this.creating = event.type === 'drawend';

      this.selectedFeature = this.creating ? event.feature : event;
      const geometry = this.selectedFeature.getGeometry();
      this.popover.setPosition(geometry.getCoordinates());

      if (this.creating) {
        this.selectedCoordinates = this.jsonFormat
            .writeGeometryObject(geometry);
        this.selectedFeature.setStyle(this.getBoulderStyle(
            this.selectedColor.color, this.selectedDifficulty.color));
      }
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
