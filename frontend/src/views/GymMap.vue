<template>
  <map-overlay
    ref="overlay"
    :loaded="loaded"
    @close="onClosePopover"
  >
    <template
      v-if="!creating"
      #toolbar
    >
      <v-col cols="2">
        <v-btn
          id="retire-boulder"
          flat
          size="small"
          icon="mdi-package-down"
          @click="retireBoulder"
        />
      </v-col>
    </template>
    <template
      v-if="creating"
      #content
    >
      <v-row>
        <v-col>
          Difficulty:
          <color-select
            id="id-difficulty-select"
            v-model="selectedDifficulty"
            :color-options="gradeColors"
            @update:model-value="updateGrade($event)"
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
            submit-button-label="Save"
            @submitted="onSubmitted"
          />
        </v-col>
      </v-row>
    </template>
    <template
      v-else
      #content
    >
      <v-row>
        <v-col>
          <v-radio-group
            v-model="selectedAscentResult"
            label="Status"
            @change="setAscentStyle"
          >
            <v-radio
              v-for="(result, index) in ascentResults"
              :key="index"
              :label="result"
              :value="index.toString()"
            />
          </v-radio-group>
        </v-col>
      </v-row>
      <v-spacer />
      <v-row>
        <v-col>
          <v-btn
            id="save-boulder"
            @click="reportAscent"
          >
            <div>save</div>
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </map-overlay>
  <div
    id="map-root"
    ref="map-root"
  />
</template>

<script>
/** @file view with interactive gym map */

import {mapActions, mapMutations, mapState} from 'vuex';
import {Collection} from 'ol';
import {containsCoordinate, getCenter} from 'ol/extent';
import {GeoJSON} from 'ol/format';
import {Draw} from 'ol/interaction';
import {Image as ImageLayer, Vector as VectorLayer} from 'ol/layer';
import Map from 'ol/Map';
import {Projection} from 'ol/proj';
import {ImageStatic, Vector as VectorSource} from 'ol/source';
import {Circle, Fill, Icon, Stroke, Style} from 'ol/style';
import View from 'ol/View';
import ColorSelect from '../components/ColorSelect.vue';
import MapOverlay from '../components/MapOverlay.vue';
import VueForm from '../components/VueForm.vue';

const defaultColor = {
  name: '',
  id: -1,
  color: '#ffffff',
};

export default {
  name: 'GymMap',
  components: {
    MapOverlay,
    VueForm,
    ColorSelect,
  },
  data() {
    return {
      gym: {
        map: '',
        id: 0,
        grade_set: [{
          id: -1,
          grade: 0,
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
      selectedBoulder: {ascent: undefined},
      selectedAscentResult: null,
      ascentIcons: [
        {
          name: 'target-circle', scale: 0.64,
        },
        {
          name: 'check-circle', scale: 0.7,
        },
        {
          name: 'check-underline-circle', scale: 0.7,
        },
      ].map(({name, scale}) => new Icon({
        src: this.axios.defaults.baseURL +
            `static/bouldern/images/${name}.svg`,
        color: '#FFFFFF',
        anchor: [0, 0],
        scale: scale,
      })),
    };
  },
  computed: {
    ...mapState({
      authToken: 'authToken',
      activeGym: 'activeGym',
    }),
    /**
     * Selectable options for the result of an attempt to ascent a boulder.
     *
     * @returns {string[]} array of selectable options
     */
    ascentResults() {
      return [0, 1, 2].map((i) => this.$t(`ascentResults[${i}]`));
    },
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
     * The options for the grade of newly created boulders
     *
     * @returns {{color: *, name: *, id: *}[]} the grade options
     */
    gradeColors() {
      return this.gym.grade_set.map(
          ({id, grade, color}) => (
            {color: color.color, id: id, name: grade + 1}));
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
      map.addOverlay(this.$refs.overlay.popover);
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
      this.$refs.overlay.close();
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
     * Sets the color style (hold and difficulty color) of the selected boulder
     *
     * @param holdColor the hold color to set
     * @param difficultyColor the difficulty color to set
     */
    setColorStyle(holdColor, difficultyColor) {
      const style = this.selectedBoulder.getStyle();
      style[1] = this.getColorStyle(holdColor, difficultyColor);
      this.selectedBoulder.setStyle(style);
    },
    /**
     * Sets the ascent style of the selected boulder according to the currently
     * selected ascent status
     */
    setAscentStyle() {
      const style = this.selectedBoulder.getStyle();
      style[2] = new Style({
        image: this.ascentIcons[this.selectedAscentResult],
      });
      this.selectedBoulder.setStyle(style);
    },
    /**
     * If the selected boulder is already associated with an ascent status,
     * and the status has changed, updates the ascent status for the boulder
     * and user via an api call and assigns the status to the selected boulder.
     * Otherwise, if the selected boulder is not yet associated with an ascent
     * status, creates a new ascent object and associates its id with the
     * selected boulder. Finally, closes the edit popover.
     */
    reportAscent() {
      const ascentApiPath = `/bouldern/gym/${this.gym.id}/boulder/` +
          `${this.selectedBoulder.id}/ascent/`;
      if (this.selectedBoulder.ascent !== undefined) {
        // only update ascent result if it has changed
        if (this.selectedAscentResult !==
            this.selectedBoulder.ascent.result.toString()) {
          this.requestWithJwt({
            apiPath: `${ascentApiPath}${this.selectedBoulder.ascent.id}/`,
            data: {'result': this.selectedAscentResult},
            method: 'PUT',
          });
          this.selectedBoulder.ascent.result = this.selectedAscentResult;
          this.$refs.overlay.close();
        }
        //  If there was no ascent entry yet, create a new one
      } else {
        this.requestWithJwt({
          apiPath: ascentApiPath,
          data: {'result': this.selectedAscentResult},
        }).then((response) => {
          this.selectedBoulder.ascent = response.data;
          this.$refs.overlay.close();
        });
      }
    },
    /**
     * Checks if the map has a boulder at the provided pixel
     *
     * @param pixel [X, Y] array to check at whether there is a boulder
     * @returns {boolean} whether there is a boulder at the pixel or not
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
        Promise.all([
          this.requestWithJwt({
            method: 'GET',
            apiPath: `/bouldern/gym/${this.gym.id}/boulder/?is_active=true`,
          }),
          this.requestWithJwt({
            method: 'GET',
            apiPath: `/bouldern/gym/${this.gym.id}/boulder/_/ascent/`,
          }),
        ]).then(([boulderResponse, ascentResponse]) => {
          this.boulders = boulderResponse.data;
          this.boulders.forEach((boulder) => {
            boulder.ascent = ascentResponse.data
                .find((ascent) => ascent.boulder === boulder.id);
          });
          // Populate with initial features
          this.boulders.forEach((boulder) => {
            const feature = this.jsonFormat.readFeature(boulder.coordinates);
            feature.id = boulder.id;
            feature.ascent = boulder.ascent;
            feature.setStyle(this.getBoulderStyle(
                boulder.color.color,
                boulder.difficulty.color.color,
                boulder.ascent ? boulder.ascent.result : undefined,
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
     * Gets the openlayers style for a boulder with the given hold and
     * difficulty color. The style is a cirle with four small border segments
     * where the cirle is colored in the boulder's difficulty color and the
     * border segments are colored in the boulder's hold color.
     *
     * @param holdColor the hold color to use for the style
     * @param difficultyColor the difficulty color to use for the style
     * @returns {Style} the color style
     */
    getColorStyle: function(holdColor, difficultyColor) {
      return new Style({
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
    },
    /**
     * Generates the openlayers style for a boulder with the given hold color,
     * difficulty color, and ascent status. The style consists of three layers:
     * - A shadow for 3D effect
     * - The color style with difficulty- and hold color.
     * - The ascent status icon
     *
     * @param holdColor the boulder's hold color
     * @param difficultyColor the boulder's difficulty color
     * @param [ascentStatus] the boulder's ascent status
     * @returns {Style[]} the boulder's style consisting of the two-colored
     * color icon, the ascent status icon, and a shadow
     */
    getBoulderStyle(holdColor, difficultyColor, ascentStatus) {
      const colorStyle = this.getColorStyle(holdColor, difficultyColor);
      const ascentStyle = ascentStatus !== undefined ?
          new Style({
            image: this.ascentIcons[ascentStatus],
          }) : new Style({});
      return [this.shadowStyle, colorStyle, ascentStyle];
    },
    /**
     * Adjusts the currently selected hold color when selecting a grade
     * and Updates both the hold and difficulty color of the most recently
     * added boulder to the provided event's color
     */
    updateGrade(event) {
      this.setColorStyle(event.color, event.color);
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
      this.setColorStyle(event.color, this.selectedDifficulty.color);
    },
    /**
     * If in create mode, removes the popover's feature from the
     * featureCollection, otherwise resets ascent status if it was changed. Then
     * (always) blurs the popover.
     */
    onClosePopover() {
      if (this.creating) {
        if (this.selectedBoulder.id === undefined) {
          this.featureCollection.pop();
        }
      } else {
        if (this.selectedBoulder.ascent !== undefined) {
          if (this.selectedBoulder.ascent.result.toString() !==
              this.selectedAscentResult) {
            this.selectedAscentResult =
                this.selectedBoulder.ascent.result.toString();
            this.setAscentStyle();
          }
        } else {
          if (this.selectedAscentResult !== null) {
            this.selectedAscentResult = null;
            this.setAscentStyle();
          }
        }
      }
    },
    /**
     * Sets the selected boulder inactive via an api call, removes it from the
     * feature collection, and closes the edit popover
     */
    retireBoulder() {
      this.requestWithJwt({
        apiPath: `/bouldern/gym/${this.gym.id}/boulder/` +
            `${this.selectedBoulder.id}/`,
        method: 'PATCH',
        data: {'is_active': false},
      });
      this.featureCollection.remove(this.selectedBoulder);
      this.$refs.overlay.close();
    },
    /**
     * Sets the selected boulder's id to the created one's and closes the
     * create popover
     */
    onSubmitted(response) {
      this.selectedBoulder.id = response.data.id;
      this.$refs.overlay.close();
    },
    /**
     * Opens the create / edit popover and closes the old one if still open. If
     * called with draw event sets selected coordinates to the event's feature's
     * coordinates and sets the drawn feature's style to the selected colors.
     *
     * @param event the draw event or the clicked feature
     */
    openPopover(event) {
      this.creating = event.type === 'drawend';

      this.selectedBoulder = this.creating ? event.feature : event;
      const geometry = this.selectedBoulder.getGeometry();

      if (this.creating) {
        this.selectedCoordinates = this.jsonFormat
            .writeGeometryObject(geometry);
        this.selectedBoulder.setStyle(this.getBoulderStyle(
            this.selectedColor.color, this.selectedDifficulty.color));
      } else {
        this.selectedAscentResult = this.selectedBoulder.ascent ?
            this.selectedBoulder.ascent.result.toString() : null;
      }
      this.$refs.overlay.open(geometry.getCoordinates());
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
</style>
