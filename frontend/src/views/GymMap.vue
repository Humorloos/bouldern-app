<template>
  <app-view v-if="editingGym">
    <template #app-bar-left>
      <v-btn
        id="close-edit-gym"
        flat
        icon="mdi-arrow-left"
        @click="editingGym = false"
      />
      <v-app-bar-title>Edit Gym</v-app-bar-title>
    </template>
    <template #main>
      <v-container>
        <gym-form
          ref="gymForm"
          :editing="true"
          :initial-data="gym"
        />
        <v-btn
          id="id_save-gym"
          @click="updateGymGrades"
        >
          Save
        </v-btn>
      </v-container>
    </template>
  </app-view>
  <app-view v-else-if="filtering">
    <template #app-bar-left>
      <v-btn
        id="close-filter"
        flat
        icon="mdi-arrow-left"
        @click="filtering = false"
      />
      <v-app-bar-title>Filter Grades</v-app-bar-title>
    </template>
    <template #main>
      <v-container fluid>
        <v-row>
          <v-col cols="1">
            <v-checkbox
              v-model="allGradesActive"
              label="all"
              hide-details
              @update:model-value="selectGrades"
            />
            <v-checkbox
              v-for="grade in gym.grade_set"
              :key="grade.id"
              v-model="activeGrades"
              :value="grade.id"
              :label="grade.grade.toString()"
              :color="getHexColor(grade.color)"
              hide-details
            />
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
  <app-view
    v-else
  >
    <template #app-bar-right>
      <v-btn
        id="id_edit_gym"
        flat
        icon="mdi-pencil"
        @click="editGym"
      />
      <v-btn
        id="id_favorite"
        flat
        icon
        @click="setFavorite"
      >
        <v-icon v-if="favorite">
          mdi-star
        </v-icon>
        <v-icon v-else>
          mdi-star-outline
        </v-icon>
      </v-btn>
      <v-btn
        id="filter"
        flat
        icon="mdi-filter"
        @click="filtering=true"
      />
    </template>
    <template #main>
      <map-overlay
        ref="overlay"
        @close="onClosePopover"
      >
        <template
          v-if="!creating"
          #toolbar-left
        >
          <v-col
            class="text-caption"
            cols="8"
            align-self="center"
          >
            Added {{ selectedBoulder.age }} day(s) ago
          </v-col>
        </template>
        <template
          v-if="!creating"
          #toolbar-right
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
              Grade:
              <color-select
                id="id-grade-select"
                v-model="selectedGrade"
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
          <vue-form
            :api-path="`/bouldern/gym/${gym.id}/boulder/`"
            :form="{
              coordinates: selectedCoordinates,
              color: selectedColor.id,
              grade: selectedGrade.id,
            }"
            submit-button-label="Save"
            @submitted="onSubmitted"
          />
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
import {Collection, Kinetic} from 'ol';
import {containsCoordinate, getCenter} from 'ol/extent';
import {GeoJSON} from 'ol/format';
import {
  defaults as defaultInteractions,
  DragPan,
  Draw,
  Modify,
  PinchRotate,
} from 'ol/interaction';
import {Image as ImageLayer, Vector as VectorLayer} from 'ol/layer';
import Map from 'ol/Map';
import {Projection} from 'ol/proj';
import {ImageStatic, Vector as VectorSource} from 'ol/source';
import {Circle, Fill, Icon, Stroke, Style, Text} from 'ol/style';
import View from 'ol/View';
import ColorSelect from '../components/ColorSelect.vue';
import MapOverlay from '../components/MapOverlay.vue';
import VueForm from '../components/VueForm.vue';
import AppView from '../components/AppView.vue';
import {
  computed,
  getCurrentInstance,
  onMounted,
  ref,
  watch,
  watchPostEffect,
} from 'vue';
import GymForm from '../components/GymForm.vue';
import {Colors} from '../constants/color.js';

export default {
  name: 'GymMap',
  components: {
    AppView,
    MapOverlay,
    VueForm,
    ColorSelect,
    GymForm,
  },
  setup() {
    const store = useStore();
    const requestWithJwt = (options) =>
      store.dispatch('requestWithJwt', options);
    const axios = store.state.axios;

    const mapRoot = ref(null);
    const overlay = ref(null);
    const map = new Map({
      moveTolerance: 4,
      interactions: defaultInteractions({dragPan: false}),
    });
    // increase rotation threshold to make it less sensible during zooms
    const interactions = map.getInteractions().getArray();
    const pinchRotate = interactions
        .filter((interaction) => interaction instanceof PinchRotate)[0];
    pinchRotate.set('threshold', 2);
    // Mount map and popover
    watchPostEffect(() => {
      if (mapRoot.value !== null) map.setTarget(mapRoot.value);
    });
    watchPostEffect(() => {
      if (overlay.value !== null) {
        const overlays = map.getOverlays();
        if (overlays.getLength() > 0) map.removeOverlay(overlays.pop());
        map.addOverlay(overlay.value.popover);
      }
    });

    onMounted(() => {
      // Make the component available to cypress in test runs
      if (window.Cypress) {
        const instance = getCurrentInstance();
        window[instance.type.name] = instance.proxy;
      }
    });

    // colors
    const colorOptions = computed(() => store.state.colors);

    // gym map
    const gym = ref({
      map: '',
      id: 0,
      grade_set: [{
        id: -1,
        grade: 0,
        color: 0,
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
    const boulderRadius = 10;

    /**
     * Gets the openlayers style for a boulder with the given hold and
     * grade color. The style is a cirle with four small border segments
     * where the cirle is colored in the boulder's grade color and the
     * border segments are colored in the boulder's hold color.
     *
     * @param holdColor the hold color to use for the style
     * @param gradeColor the grade color to use for the style
     * @returns {Style} the color style
     */
    function getColorStyle(holdColor, gradeColor) {
      return new Style({
        image: new Circle({
          fill: new Fill({
            color: gradeColor,
          }),
          stroke: new Stroke({
            color: holdColor,
            width: 6,
            lineDash: [7.4, 8.05],
            lineDashOffset: 3.45,
          }),
          radius: boulderRadius,
        }),
      });
    }
    const shadowStyle = new Style({
      image: new Icon({
        src: axios.defaults.baseURL +
            'static/bouldern/images/shadow.png',
        scale: 0.34,
        opacity: 0.6,
        color: 'Black',
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

    const invisible = new Style({});

    /**
     * Generates the openlayers style for a boulder with the given hold color,
     * grade color, and ascent status. The style consists of three
     * layers:
     * - A shadow for 3D effect
     * - The color style with grade- and hold color.
     * - The ascent status icon
     *
     * @param holdColor the boulder's hold color
     * @param gradeColor the boulder's grade color
     * @param age the boulder's age in days
     * @param [ascentStatus] the boulder's ascent status
     * @returns {Style[]} the boulder's style consisting of the two-colored
     * color icon, the age in days, the ascent status icon, and a shadow
     */
    function getBoulderStyle(holdColor, gradeColor, age, ascentStatus) {
      const colorStyle = getColorStyle(holdColor, gradeColor);
      const ascentStyle = ascentStatus === undefined ? invisible :
          new Style({
            image: ascentIcons[ascentStatus],
          });
      const ageStyle = new Style({
        text: new Text({
          fill: new Fill({color: '#FFFFFF'}),
          stroke: new Stroke({
            color: '#000000',
            width: 2,
          }),
          offsetX: -10,
          offsetY: 10,
          text: age.toString(),
        }),
      });
      return [shadowStyle, colorStyle, ascentStyle, ageStyle];
    }


    /**
     * Checks if the map has a boulder at the provided pixel
     *
     * @param pixel [X, Y] array to check at whether there is a boulder
     * @returns {boolean} whether there is a boulder at the pixel or not
     */
    function hasBoulderAtPixel(pixel) {
      return map.hasFeatureAtPixel(pixel, {
        layerFilter: (layer) => layer
            .getClassName() === vectorLayer.getClassName(),
      });
    }

    const jsonFormat = ref(new GeoJSON());

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
    const mapImage = new Image();

    /**
     * Sets the image layer's source's image to the loaded map image
     */
    function setMapImage(image) {
      image.setImage(mapImage);
    }

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
        imageLoadFunction: setMapImage,
      });
    });
    /**
     * This layer contains the map image
     *
     * @returns {ImageLayer} the map image layer
     */
    const imageLayer = new ImageLayer({className: 'image-layer'});
    /**
     * Icon drawing interaction for drawing boulder icons. Only allows drawing
     * on the image, not outside of it.
     *
     * @returns {Draw} the draw interaction
     */
    const drawInteraction = new Draw({
      type: 'Point',
      source: vectorSource,
      style: invisible,
      dragVertexDelay: 99999999,
      condition: (event) => {
        return containsCoordinate(extent, event.coordinate) &&
            !hasBoulderAtPixel(event.pixel);
      },
    });

    // interaction for moving boulders
    const modifyTouchThreshold = 500;
    const modifyInteraction = new Modify({
      source: vectorSource,
      style: invisible,
      pixelTolerance: 20,
      condition: (event) => {
        // on touch screen, start moving only after holding for some time
        if (event.originalEvent.pointerType === 'touch') {
          return getEventDelay(event) >= modifyTouchThreshold;
        } else {
          return hasBoulderAtPixel(event.pixel);
        }
      },
    });
    const moving = ref(false);
    const dragPanInteraction = new DragPan({
      condition: (event) => {
        return getEventDelay(event) < modifyTouchThreshold;
      },
      kinetic: new Kinetic(-0.005, 0.05, 100),
    });

    /**
     * Gets the color associated to the provided ID.
     *
     * @param colorId the id to get the color for
     * @returns {string} the color string
     */
    function getHexColor(colorId) {
      return store.getters.colorById(colorId).color;
    }

    /**
     * Gets the grade object associated to the provided ID.
     *
     * @param gradeId the id to get the grade for.
     * @returns {object} the grade object.
     */
    function getGrade(gradeId) {
      const grade = gym.value.grade_set.find((g) => g.id === gradeId);
      if (grade === undefined) return defaultGrade;
      return grade;
    }

    const defaultGrade = {
      grade: -1,
      id: -1,
      color: -1,
    };
    /**
     * Sets the style of the provided boulder feature based on its color, grade,
     * and ascent result
     *
     * @param boulder the boulder to set the style of
     */
    function setBoulderStyle(boulder) {
      boulder.setStyle(getBoulderStyle(
          getHexColor(boulder.color),
          getHexColor(getGrade(boulder.grade).color),
          boulder.age,
          boulder.ascent !== null ? boulder.ascent.result : undefined,
      ));
    }

    // favorite gym toggle
    const favorite = ref(false);

    /**
     * Gets the gym data from the API, loads the gym map image, and deserializes
     * the gym's boulders into the feature collection
     */
    function loadGymMap(onLoaded) {
      requestWithJwt({
        method: 'GET',
        apiPath: `/bouldern/gym-map-resources/?name=${gymName.value}`,
      }).then((response) => {
        gym.value = response.data['gym'];
        // set all grades active
        activeGrades.value = gym.value.grade_set.map((grade) => grade.id);
        // Load boulders
        response.data.boulder_features.forEach((featureData) => {
          const boulderData = featureData.boulder;
          const boulder = Object.assign(
              jsonFormat.value.readFeature(boulderData.coordinates),
              (({id, color, grade, age}) => ({
                id,
                color,
                grade,
                age,
                ascent: featureData.ascent,
              }))(boulderData));
          setBoulderStyle(boulder);
          vectorSource.addFeature(boulder);
        });
        // load map
        mapImage.onload = () => {
          // set map image layer
          extent[2] = mapImage.naturalWidth;
          extent[3] = mapImage.naturalHeight;
          imageLayer.setSource(mapImageSource.value);
          map.setLayers([
            imageLayer,
            vectorLayer,
          ]);
          map.setView(new View({
            projection: projection.value,
            center: getCenter(extent),
            zoom: 1,
            maxZoom: 8,
          }));
          if (onLoaded) onLoaded();
        };
        mapImage.src = gym.value.map;
      });
      favorite.value = store.state.favoriteGyms.includes(gymName.value);
    }

    const loaded = ref(false);

    // create popover

    const creating = ref(false);

    const selectedBoulder = ref({ascent: undefined});
    const selectedCoordinates = ref({});
    const selectedColor = ref(Colors.DEFAULT_COLOR);
    const selectedGrade = ref(Colors.DEFAULT_COLOR);

    /**
     * Opens the create popover and closes the old one if still open. Sets
     * selected coordinates to the event's feature's
     * coordinates and sets the drawn feature's style to the selected colors.
     *
     * @param event the draw event
     */
    function openCreatePopover(event) {
      overlay.value.close();
      creating.value = true;

      const feature = event.feature;
      feature.ascent = null;
      const geometry = feature.getGeometry();

      selectedCoordinates.value = jsonFormat.value
          .writeGeometryObject(geometry);
      feature.setStyle(getBoulderStyle(
          selectedColor.value.color, selectedGrade.value.color, '0'));

      selectedBoulder.value = feature;
      overlay.value.open(geometry.getCoordinates());
    }

    // reset selected colors and close popover when changing gym
    watch(gymName, () => {
      selectedGrade.value = Colors.DEFAULT_COLOR;
      selectedColor.value = Colors.DEFAULT_COLOR;
      overlay.value.close();
    });

    /**
     * Sets the color style (hold and grade color) of the selected boulder
     *
     * @param holdColor the hold color to set
     * @param gradeColor the grade color to set
     */
    function setColorStyle(holdColor, gradeColor) {
      const style = selectedBoulder.value.getStyle();
      style[1] = getColorStyle(holdColor, gradeColor);
      selectedBoulder.value.setStyle(style);
    }

    /**
     * Adjusts the currently selected hold color when selecting a grade
     * and Updates both the hold and grade color of the most recently
     * added boulder to the provided event's color
     *
     * @param selectedOption the selected color Option
     */
    function updateGrade(selectedOption) {
      setColorStyle(selectedOption.color, selectedOption.color);
      selectedColor.value = colorOptions.value.filter(
          (colorOption) => colorOption.color === selectedOption.color)[0];
    }

    /**
     * Updates the hold color of the most recently added boulder to the provided
     * event's color
     *
     * @param selectedOption the selected color Option
     */
    function updateHoldColor(selectedOption) {
      setColorStyle(selectedOption.color, selectedGrade.value.color);
    }

    /**
     * The options for the grade of newly created boulders
     *
     * @returns {{color: *, name: *, id: *}[]} the grade options
     */
    const gradeColors = computed(() => {
      return gym.value.grade_set.map(
          ({id, grade, color}) => ({
            color: getHexColor(color),
            id: id,
            name: grade,
          }));
    });

    /**
     * Sets the selected boulder's id to the created one's and closes the
     * create popover
     */
    function onSubmitted(response) {
      selectedBoulder.value.id = response.data.id;
      selectedBoulder.value.grade = response.data.grade;
      selectedBoulder.value.color = response.data.color;
      selectedBoulder.value.age = 0;
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

    // Edit popover
    const selectedAscentResult = ref(null);

    /**
     * Opens the edit popover and closes the old one if still open.
     *
     * @param feature the clicked boulder
     */
    function openEditPopover(feature) {
      overlay.value.close();
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
     * Submits the selected ascent result and closes the edit popover.
     */
    function reportAscent() {
      requestWithJwt({
        apiPath: `/bouldern/gym/${gym.value.id}/boulder/` +
            `${selectedBoulder.value.id}/ascent/`,
        data: {'result': selectedAscentResult.value},
      }).then((response) => {
        selectedBoulder.value.ascent = response.data;
        overlay.value.close();
      });
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
        method: 'DELETE',
      });
      featureCollection.remove(featureCollection.getArray()
          .find((feature) => feature.id === selectedBoulder.value.id));
      overlay.value.close();
    }

    /**
     * Resets ascent status if it was changed.
     */
    function onCloseEditPopover() {
      if (selectedBoulder.value.ascent !== null) {
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

    /**
     * calls close popover handler for create / edit popover
     */
    function onClosePopover() {
      if (creating.value) onCloseCreatePopover();
      else onCloseEditPopover();
    }

    // filtering by grade

    const filtering = ref(false);

    const allGradesActive = ref(true);

    /**
     * Sets all grades active / inactive when toggling "all" checkbox
     */
    function selectGrades(allGradesActive) {
      if (allGradesActive) {
        activeGrades.value = gym.value.grade_set.map((grade) => grade.id);
      } else activeGrades.value = [];
    }

    const activeGrades = ref([]);

    // set boulders of filtered grades invisible and those of active grades
    // visible
    watch(activeGrades, () => {
      featureCollection.forEach((boulder) => {
        // if boulder's grade is active and boulder is invisible, show it
        if (activeGrades.value.includes(boulder.grade)) {
          if (boulder.getStyle().length === undefined) {
            setBoulderStyle(boulder);
          }
          //  if boulder's grade is inactive and boulder is visible, hide it
        } else {
          if (boulder.getStyle().length !== undefined) {
            boulder.setStyle(invisible);
          }
        }
      });
    });

    // loading gym map
    const grabbingBoulder = ref(false);
    let timer;

    /**
     * todo
     */
    function getDelay(timeStamp) {
      return performance.now() - timeStamp;
    }

    /**
     * todo
     */
    function getEventDelay(event) {
      return getDelay(event.originalEvent.timeStamp);
    }

    /**
     * todo
     */
    function setCursorStyle(style) {
      map.getViewport().style.cursor = style;
    }

    /**
     * todo
     */
    function getBoulderAtPixel(pixel) {
      const boulder = map
          .forEachFeatureAtPixel(pixel, (feature) => feature);
      if (boulder && boulder.getStyle() !== invisible) {
        return boulder;
      }
      return undefined;
    }

    /**
     * todo
     */
    function setBoulderRadius(boulder, radius) {
      const style = boulder.getStyle();
      const colorStyle = style[1].getImage();
      colorStyle.setRadius(radius);
      style[1].setImage(colorStyle);
      boulder.setStyle(style);
    }

    const clickStart = ref(NaN);

    /**
     * Sets the loaded flag and initializes the map
     */
    function onGymMapLoaded() {
      drawInteraction.on('drawend', openCreatePopover);
      map.addInteraction(drawInteraction);
      map.addInteraction(dragPanInteraction);

      let initialBoulderCoordinates;
      modifyInteraction.on('modifystart', (event) => {
        initialBoulderCoordinates = event.features.getArray()[0]
            .getGeometry().getCoordinates();
        // deactivate drag pan
        dragPanInteraction.setActive(false);
        setCursorStyle('grabbing');
        grabbingBoulder.value = true;
      });
      modifyInteraction.on('modifyend', (event) => {
        const boulder = event.features.getArray()[0];
        if (event.mapBrowserEvent.originalEvent.pointerType === 'touch') {
          setBoulderRadius(boulder, boulderRadius);
        }
        const boulderGeometry = boulder.getGeometry();
        if (!containsCoordinate(extent, boulderGeometry.getCoordinates())) {
          boulderGeometry.setCoordinates(initialBoulderCoordinates);
        } else {
          requestWithJwt({
            apiPath: `/bouldern/gym/${gym.value.id}/boulder/` +
            `${boulder.id}/`,
            method: 'PATCH',
            data: {
              coordinates: jsonFormat.value
                  .writeGeometryObject(boulderGeometry),
            },
          });
        }
        dragPanInteraction.setActive(true);
        grabbingBoulder.value = false;
      });
      map.addInteraction(modifyInteraction);

      // fire pointerdown events a second time after some delay to tigger moving
      // boulders on touch screens
      map.on('pointerdown', (event) => {
        clickStart.value = event.originalEvent.timeStamp;
        const boulder = getBoulderAtPixel(event.pixel);
        if (boulder) {
          if (event.originalEvent.pointerType === 'touch') {
            timer = setTimeout(() => {
              // fire event only once and only if not panning the map
              if (getEventDelay(event) < 2 * modifyTouchThreshold &&
                  !moving.value) {
                setBoulderRadius(boulder, 35);
                map.mapBrowserEventHandler_.dispatchEvent(event);
              }
            },
            modifyTouchThreshold,
            );
          } else {
            setCursorStyle('grabbing');
            grabbingBoulder.value = true;
          }
        }
      });
      map.on('pointerup', (event) => {
        if (hasBoulderAtPixel(event.pixel)) {
          setCursorStyle('');
          grabbingBoulder.value = false;
        }
        clearTimeout(timer);
      });
      map.on('click', (event) => {
        const boulder = getBoulderAtPixel(event.pixel);
        if (boulder) {
          if (getDelay(clickStart.value) >= modifyTouchThreshold) {
            setBoulderRadius(boulder, boulderRadius);
          } else {
            openEditPopover(boulder);
          }
        }
      });
      map.on('pointermove', (event) => {
        const pixel = map.getEventPixel(event.originalEvent);
        const hit = hasBoulderAtPixel(pixel);
        setCursorStyle(hit ?
            grabbingBoulder.value ? 'grabbing' :
                'pointer' : '');
      });
      map.on('movestart', () => {
        moving.value = true;
      });
      map.on('moveend', () => {
        moving.value = false;
      });
      loaded.value = true;
    }

    loadGymMap(onGymMapLoaded);
    // Load new gym map when gym name changes
    watch(gymName, (newGymName) => {
      featureCollection.clear();
      if (newGymName !== null) {
        loadGymMap();
      }
    });

    /**
     * Creates/removes a favorite gym entry for this gym
     */
    function setFavorite() {
      favorite.value = !favorite.value;
      if (favorite.value) store.dispatch('addFavoriteGym', gymName.value);
      else store.dispatch('removeFavoriteGym', gymName.value);
    }

    // edit gym view

    const gymForm = ref(null);
    const editingGym = ref(false);

    /**
     * Opens the edit gym view
     */
    function editGym() {
      editingGym.value = true;
    }

    /**
     * Updates the gym's grades via PATCH request with the grades from the gym
     * form
     */
    function updateGymGrades() {
      requestWithJwt({
        apiPath: `bouldern/gym/${gym.value.id}/`,
        method: 'PATCH',
        data: {grade_set: gymForm.value.grades},
      }).then((response) => {
        gym.value = response.data;
        vectorSource.forEachFeature((boulder) => {
          if (gymForm.value.gradeIds.includes(boulder.grade)) {
            setBoulderStyle(boulder);
          } else {
            vectorSource.removeFeature(boulder);
          }
        });
        editingGym.value = false;
      });
    }

    return {
      // colors
      getHexColor,
      // gym map
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
      selectedGrade,
      updateGrade,
      updateHoldColor,
      onSubmitted,
      // edit popover
      selectedBoulder,
      selectedAscentResult,
      setAscentStyle,
      retireBoulder,
      reportAscent,
      onClosePopover,
      // filter
      filtering,
      allGradesActive,
      selectGrades,
      activeGrades,
      // favorite
      favorite,
      setFavorite,
      // gym name
      gymName,
      // edit gym
      editGym,
      editingGym,
      gymForm,
      updateGymGrades,
      // moving boulders
      modifyTouchThreshold,
    };
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
