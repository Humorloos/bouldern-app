<template>
  <app-view>
    <template #main>
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
        ref="mapRoot"
      />
    </template>
  </app-view>
</template>

<script>
/** @file view with interactive gym map */

import {useStore} from 'vuex';
import {useRoute} from 'vue-router';
import {useI18n} from 'vue-i18n';
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
import AppView from '../components/AppView.vue';
import {computed, getCurrentInstance, onMounted, ref, watch} from 'vue';

export default {
  name: 'GymMap',
  components: {
    AppView,
    MapOverlay,
    VueForm,
    ColorSelect,
  },
  setup() {
    // ############ used so often don't know that to do with it yet ####
    const store = useStore();
    const requestWithJwt = (options) =>
      store.dispatch('requestWithJwt', options);
    const axios = store.state.axios;

    // ############ mounted
    // Make the component available to cypress in test runs
    onMounted(() => {
      if (window.Cypress) {
        const instance = getCurrentInstance();
        window[instance.type.name] = instance.proxy;
      }
    });

    // ############ loading the gym map
    const defaultColor = {
      name: '',
      id: -1,
      color: '#ffffff',
    };
    const gym = ref({
      map: '',
      id: 0,
      grade_set: [{
        id: -1,
        grade: 0,
        color: defaultColor,
      }],
    });
    const route = useRoute();
    /**
     * Gets the name of the gym to show the map of and sets it as the active gym
     * if a new gym was opened
     *
     * @returns {string} the name of the gym of which to show the map
     */
    const gymName = computed(() => {
      if (route.matched.some(({name}) => name === 'gymMap')) {
        const gymName = route.params.gymName;
        store.commit('setActiveGym', gymName);
        return gymName;
      } else {
        return store.state.activeGym;
      }
    });
    const featureCollection = new Collection();
    // Vector source to draw boulders on
    const vectorSource = new VectorSource({
      features: featureCollection,
      useSpatialIndex: false, // improves performance
    });
    // This layer is where icons are drawn on
    const vectorLayer = new VectorLayer({
      className: 'vector-layer',
      source: vectorSource,
      updateWhileAnimating: true,
      updateWhileInteracting: true,
    });

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
    function getColorStyle(holdColor, difficultyColor) {
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
    }

    const shadowStyle = new Style({
      image: new Icon({
        src: axios.defaults.baseURL +
            'static/bouldern/images/shadow.png',
        scale: 0.34,
        opacity: 0.6,
      }),
    });
    const ascentIcons = [
      {name: 'target-circle', scale: 0.64},
      {name: 'check-circle', scale: 0.7},
      {name: 'check-underline-circle', scale: 0.7},
    ].map(({name, scale}) => new Icon({
      src: axios.defaults.baseURL +
          `static/bouldern/images/${name}.svg`,
      color: '#FFFFFF',
      anchor: [0, 0],
      scale: scale,
    }));

    /**
     * Generates the openlayers style for a boulder with the given hold color,
     * difficulty color, and ascent status. The style consists of three
     * layers:
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
    function getBoulderStyle(holdColor, difficultyColor, ascentStatus) {
      const colorStyle = getColorStyle(holdColor, difficultyColor);
      const ascentStyle = ascentStatus !== undefined ?
          new Style({
            image: ascentIcons[ascentStatus],
          }) : new Style({});
      return [shadowStyle, colorStyle, ascentStyle];
    }

    const mapRoot = ref(null);
    /**
     * Initializes the gym map with image layer, vector layer, popover, and
     * draw interaction
     *
     * @returns {Map} the gym map
     */
    const map = computed(() => {
      // Initialize map
      const map = new Map({
        target: mapRoot.value,
      });
      map.addOverlay(overlay.value.popover);
      map.on('pointermove', (event) => {
        const pixel = map.getEventPixel(event.originalEvent);
        const hit = hasBoulderAtPixel(pixel);
        map.getTarget().style.cursor = hit ? 'pointer' : '';
      });
      return map;
    });
    const jsonFormat = ref(new GeoJSON());

    /**
     * Checks if the map has a boulder at the provided pixel
     *
     * @param pixel [X, Y] array to check at whether there is a boulder
     * @returns {boolean} whether there is a boulder at the pixel or not
     */
    function hasBoulderAtPixel(pixel) {
      return map.value.hasFeatureAtPixel(pixel, {
        layerFilter: (layer) => layer
            .getClassName() === vectorLayer.getClassName(),
      });
    }

    const extent = [0, 0, 0, 0];
    /**
     * Projecton from image coordinates to geo-coordinates
     *
     * @returns {Projection} the projection
     */
    const projection = computed(() => {
      return new Projection({
        code: 'xkcd-image',
        units: 'pixels',
        extent: extent,
      });
    });
    /**
     * The openlayers gym map image source to be used in the image layer.
     *
     * @returns {ImageStatic} the map image source.
     */
    const mapImageSource = computed(() => {
      return new ImageStatic({
        url: gym.value.map,
        projection: projection.value,
        imageExtent: extent,
        imageLoadFunction: (image) => image.setImage(mapImage),
      });
    });
    /**
     * This layer contains the map image
     *
     * @returns {ImageLayer} the map image layer
     */
    const imageLayer = computed(() => {
      return new ImageLayer({
        className: 'image-layer',
        source: mapImageSource.value,
      });
    });

    /**
     * Icon drawing interaction for drawing boulder icons. Only allows drawing
     * on the image, not outside of it.
     *
     * @returns {Draw} the draw interaction
     */
    const drawInteraction = computed(() => {
      return new Draw({
        type: 'Point',
        source: vectorSource,
        style: new Style({}),
        condition: (event) => {
          return containsCoordinate(extent, event.coordinate) &&
              !hasBoulderAtPixel(event.pixel);
        },
      });
    });
    const mapImage = new Image();

    /**
     * Gets the gym data from the API, loads the gym map image, and deserializes
     * the gym's boulders into the feature collection
     */
    function loadGymMap(onLoaded) {
      requestWithJwt({
        method: 'GET',
        apiPath: `/bouldern/gym/?name=${gymName.value}`,
      }).then((response) => {
        gym.value = response.data[0];
        mapImage.src = gym.value.map;
        mapImage.onload = () => {
          extent[2] = mapImage.width;
          extent[3] = mapImage.height;
          map.value.setLayers([
            imageLayer.value,
            vectorLayer,
          ]);
          map.value.setView(new View({
            projection: projection.value,
            center: getCenter(extent),
            zoom: 1,
            maxZoom: 8,
          }));
          map.value.removeInteraction(drawInteraction.value);
          map.value.addInteraction(drawInteraction.value);
          if (onLoaded) onLoaded();
        };
        Promise.all([
          requestWithJwt({
            method: 'GET',
            apiPath: `/bouldern/gym/${gym.value.id}/boulder/?is_active=true`,
          }),
          requestWithJwt({
            method: 'GET',
            apiPath: `/bouldern/gym/${gym.value.id}/boulder/_/ascent/`,
          }),
        ]).then(([boulderResponse, ascentResponse]) => {
          const boulders = boulderResponse.data;
          boulders.forEach((boulder) => {
          // Populate with initial features
            const feature = jsonFormat.value.readFeature(boulder.coordinates);
            feature.id = boulder.id;
            const ascent = ascentResponse.data
                .find((ascent) => ascent.boulder === boulder.id);
            feature.ascent = ascent;
            feature.setStyle(getBoulderStyle(
                boulder.color.color,
                boulder.difficulty.color.color,
                ascent ? ascent.result : undefined,
            ));
            vectorSource.addFeature(feature);
          });
        });
      });
    }

    const loaded = ref(false);

    /**
     * Sets the loaded flag and initializes the
     * map
     */
    function onGymMapLoaded() {
      loaded.value = true;
      drawInteraction.value.on('drawend', openCreatePopover);
      map.value.on('click', (event) => {
        const feature = map.value
            .forEachFeatureAtPixel(event.pixel, (feature) => feature);
        if (feature) openEditPopover(feature);
      });
    }

    // load the gym map when opening this view
    loadGymMap(onGymMapLoaded);
    // Load new gym map when gym name changes
    watch(gymName, () => {
      featureCollection.clear();
      loadGymMap();
    });

    // ########## load color options for holds when opening view

    const colorOptions = ref([defaultColor]);
    requestWithJwt({
      method: 'GET',
      apiPath: `/bouldern/color/`,
    }).then((response) => {
      colorOptions.value = response.data;
    });

    /**
     * If in create mode, , otherwise . Then
     * (always) blurs the popover.
     */
    function onClosePopover() {
      if (creating.value) onCloseCreatePopover();
      else onCloseEditPopover();
    }

    // ############## create / edit popover
    // todo: separate this into openCreatePopover and openEditPopover

    const selectedBoulder = ref({ascent: undefined});
    const creating = ref(false);
    const selectedCoordinates = ref({});
    const selectedColor = ref(defaultColor);
    // todo: rename to selectedGrade
    const selectedDifficulty = ref(defaultColor);
    const selectedAscentResult = ref(null);
    const overlay = ref(null);

    /**
     * Opens the create popover and closes the old one if still open. Sets
     * selected coordinates to the event's feature's
     * coordinates and sets the drawn feature's style to the selected colors.
     *
     * @param event the draw event
     */
    function openCreatePopover(event) {
      creating.value = true;

      const feature = event.feature;
      const geometry = feature.getGeometry();

      selectedCoordinates.value = jsonFormat.value
          .writeGeometryObject(geometry);
      feature.setStyle(getBoulderStyle(
          selectedColor.value.color, selectedDifficulty.value.color));

      selectedBoulder.value = feature;
      overlay.value.open(geometry.getCoordinates());
    }

    // reset selected colors and close popover when changing gym
    watch(gymName, () => {
      selectedDifficulty.value = defaultColor;
      selectedColor.value = defaultColor;
      overlay.value.close();
    });

    /**
     * Sets the color style (hold and difficulty color) of the selected boulder
     *
     * @param holdColor the hold color to set
     * @param difficultyColor the difficulty color to set
     */
    function setColorStyle(holdColor, difficultyColor) {
      const style = selectedBoulder.value.getStyle();
      style[1] = getColorStyle(holdColor, difficultyColor);
      selectedBoulder.value.setStyle(style);
    }

    /**
     * Adjusts the currently selected hold color when selecting a grade
     * and Updates both the hold and difficulty color of the most recently
     * added boulder to the provided event's color
     */
    function updateGrade(event) {
      setColorStyle(event.color, event.color);
      selectedColor.value = colorOptions.value.filter(
          (colorOption) => colorOption.color === event.color)[0];
    }

    /**
     * Updates the hold color of the most recently added boulder to the provided
     * event's color
     *
     * @param event a color select update event
     */
    function updateHoldColor(event) {
      setColorStyle(event.color, selectedDifficulty.value.color);
    }

    /**
     * The options for the grade of newly created boulders
     *
     * @returns {{color: *, name: *, id: *}[]} the grade options
     */
    const gradeColors = computed(() => {
      return gym.value.grade_set.map(
          ({id, grade, color}) => (
            {color: color.color, id: id, name: grade}));
    });

    /**
     * Sets the selected boulder's id to the created one's and closes the
     * create popover
     */
    function onSubmitted(response) {
      selectedBoulder.value.id = response.data.id;
      overlay.value.close();
    }


    /**
     * Removes the popover's feature from the featureCollection
     */
    function onCloseCreatePopover() {
      if (selectedBoulder.value.id === undefined) {
        featureCollection.pop();
      }
    }

    // todo: when clicking on map while in edit popover, the selected boulder
    //  is removed, but it should happen the same as when closing the popover

    // ########################### edit popover

    /**
     * Opens the edit popover and closes the old one if still open.
     *
     * @param feature the clicked boulder
     */
    function openEditPopover(feature) {
      creating.value = false;
      selectedAscentResult.value = feature.ascent ?
          feature.ascent.result.toString() : null;
      selectedBoulder.value = feature;
      overlay.value.open(feature.getGeometry().getCoordinates());
    }

    /**
     * Sets the ascent style of the selected boulder according to the currently
     * selected ascent status
     */
    function setAscentStyle() {
      const style = selectedBoulder.value.getStyle();
      style[2] = new Style({
        image: ascentIcons[selectedAscentResult.value],
      });
      selectedBoulder.value.setStyle(style);
    }

    /**
     * If the selected boulder is already associated with an ascent status,
     * and the status has changed, updates the ascent status for the boulder
     * and user via an api call and assigns the status to the selected boulder.
     * Otherwise, if the selected boulder is not yet associated with an ascent
     * status, creates a new ascent object and associates its id with the
     * selected boulder. Finally, closes the edit popover.
     */
    function reportAscent() {
      const ascentApiPath = `/bouldern/gym/${gym.value.id}/boulder/` +
          `${selectedBoulder.value.id}/ascent/`;
      if (selectedBoulder.value.ascent !== undefined) {
        // only update ascent result if it has changed
        if (selectedAscentResult.value !==
            selectedBoulder.value.ascent.result.toString()) {
          requestWithJwt({
            apiPath: `${ascentApiPath}${selectedBoulder.value.ascent.id}/`,
            data: {'result': selectedAscentResult.value},
            method: 'PUT',
          });
          selectedBoulder.value.ascent.result = selectedAscentResult.value;
          overlay.value.close();
        }
        //  If there was no ascent entry yet, create a new one
      } else {
        requestWithJwt({
          apiPath: ascentApiPath,
          data: {'result': selectedAscentResult.value},
        }).then((response) => {
          selectedBoulder.value.ascent = response.data;
          overlay.value.close();
        });
      }
    }

    const {t} = useI18n();
    // Selectable options for the result of an attempt to ascend a boulder.
    const ascentResults = [0, 1, 2].map((i) => t(`ascentResults[${i}]`));

    /**
     * Sets the selected boulder inactive via an api call, removes it from the
     * feature collection, and closes the edit popover
     */
    function retireBoulder() {
      requestWithJwt({
        apiPath: `/bouldern/gym/${gym.value.id}/boulder/` +
            `${selectedBoulder.value.id}/`,
        method: 'PATCH',
        data: {'is_active': false},
      });
      featureCollection.remove(featureCollection.getArray()
          .find((feature) => feature.id === selectedBoulder.value.id));
      overlay.value.close();
    }

    /**
     * Resets ascent status if it was changed.
     */
    function onCloseEditPopover() {
      if (selectedBoulder.value.ascent !== undefined) {
        if (selectedBoulder.value.ascent.result.toString() !==
            selectedAscentResult.value) {
          selectedAscentResult.value =
              selectedBoulder.value.ascent.result.toString();
          setAscentStyle();
        }
      } else {
        if (selectedAscentResult.value !== null) {
          selectedAscentResult.value = null;
          setAscentStyle();
        }
      }
    }
    // todo: split into composition functions as here:
    // https://v3.vuejs.org/guide/composition-api-introduction.html#standalone
    // -computed-properties
    return {
      gym,
      ascentResults,
      mapRoot,
      loaded,
      colorOptions,
      overlay,
      creating,
      // create popover
      selectedCoordinates,
      selectedColor,
      gradeColors,
      selectedDifficulty,
      updateGrade,
      updateHoldColor,
      onSubmitted,
      // edit popover
      selectedAscentResult,
      setAscentStyle,
      retireBoulder,
      reportAscent,
      onClosePopover,
    };
  }
  ,
}
;
</script>

<style>
@import '../../node_modules/ol/ol.css';

#map-root {
  width: 100%;
  height: 100%;
}
</style>
