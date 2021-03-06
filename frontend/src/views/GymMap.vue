<template>
  <v-dialog v-model="deleteDialog">
    <v-card>
      <v-card-text>
        {{ $t('gymMap.deleteWarning', {gym: gym.name}) }}
      </v-card-text>
      <v-card-actions>
        <v-btn @click="deleteDialog=false">
          {{ $t('gymMap.cancel') }}
        </v-btn>
        <v-btn
          color="error"
          @click="deleteGym"
        >
          {{ $t('gymMap.deleteGym') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
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
          @save="updateGymGrades"
        />
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
              id="id_filter-all"
              v-model="allGradesActive"
              label="all"
              hide-details
              @update:model-value="selectGrades"
            />
            <v-checkbox
              v-for="(grade, index) in gym.grade_set"
              :id="`id_filter-${index + 1}`"
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
    ref="appView"
  >
    <template #app-bar-right>
      <v-btn
        id="id_favorite"
        flat
        icon
        @click="setFavorite"
      >
        <v-icon
          v-if="favorite"
          color="#E3B341"
        >
          mdi-star
        </v-icon>
        <v-icon v-else>
          mdi-star-outline
        </v-icon>
      </v-btn>
      <v-btn
        id="id_filter"
        flat
        icon="mdi-filter"
        @click="filtering=true"
      />
      <v-menu
        v-model="menu"
        anchor="bottom end"
      >
        <template #activator="{ props }">
          <v-btn
            id="id_menu"
            flat
            icon="mdi-dots-vertical"
            v-bind="props"
          />
        </template>

        <v-list>
          <v-list-item
            v-for="(item, i) in menuItems"
            :key="i"
            @click="item.callback()"
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
    <template #app-drawer>
      <v-divider />
      <v-list-item
        id="id_refresh"
        @click="refresh"
      >
        <v-icon>mdi-refresh</v-icon>
        <v-list-item-title class="pl-3">
          Refresh
        </v-list-item-title>
      </v-list-item>
      <v-divider />
    </template>
    <template #main>
      <map-overlay
        ref="overlay"
        @close="onClosePopover"
      >
        <template
          v-if="reportingAscent"
          #toolbar-left
        >
          <v-col
            class="text-caption"
            cols="6"
            align-self="center"
          >
            Added {{ selectedBoulderAge }} day(s) ago
          </v-col>
        </template>
        <template
          v-if="reportingAscent"
          #toolbar-right
        >
          <v-col cols="2">
            <v-btn
              id="id_retire-boulder"
              flat
              size="small"
              icon="mdi-package-down"
              @click="retireBoulder"
            />
          </v-col>
          <v-col cols="2">
            <v-btn
              id="id_edit-boulder"
              flat
              size="small"
              icon="mdi-pencil"
              @click="openEditPopover"
            />
          </v-col>
        </template>
        <template
          v-if="creating || editingBoulder"
          #content
        >
          <boulder-form
            :hold-color="selectedColor"
            :grade-color="selectedGradeColor"
            :grade-color-options="gradeColors"
            @update:hold-color="updateHoldColor($event)"
            @update:grade-color="updateGrade($event)"
            @save="createOrUpdateBoulder"
          />
        </template>
        <template
          v-else-if="reportingAscent"
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
        id="id_map-root"
        ref="mapRoot"
      />
    </template>
  </app-view>
</template>

<script>
/** @file view with interactive gym map */

import {useStore} from 'vuex';
import {useRoute, useRouter} from 'vue-router';
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
import MapOverlay from '../components/MapOverlay.vue';
import AppView from '../components/AppView.vue';
import {
  computed,
  getCurrentInstance,
  nextTick,
  onMounted,
  ref,
  watch,
  watchPostEffect,
} from 'vue';
import GymForm from '../components/GymForm.vue';
import {Colors} from '../constants/color.js';
import BoulderForm from '../components/BoulderForm.vue';

export default {
  name: 'GymMap',
  components: {
    AppView,
    MapOverlay,
    GymForm,
    BoulderForm,
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

    // gym map
    const defaultGym = {
      name: null,
      map: '',
      id: 0,
      grade_set: [{
        id: -1,
        grade: 0,
        color: 0,
      }],
    };
    const gym = ref(defaultGym);
    const route = useRoute();
    /**
     * Gets the name of the gym to show the map of and sets it as the active gym
     * if a new gym was opened
     *
     * @returns {string} the name of the gym of which to show the map
     */
    const gymName = computed(() => {
      return route.params.gymName;
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
          `static/boulvdern/images/${name}.svg`,
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
      return getBoulderAtPixel(pixel) !== undefined;
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
          const boulder = getBoulderAtPixel(event.pixel);
          return boulder !== undefined &&
              !isBeingEdited(boulder);
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

    const defaultGrade = {
      grade: -1,
      id: -1,
      color: -1,
    };

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

    /**
     * Sets the style of the provided boulder feature based on its color, grade,
     * and ascent result
     *
     * @param boulder the boulder to set the style of
     */
    function resetBoulderStyle(boulder) {
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
    function loadGymMap(onMapLoaded) {
      requestWithJwt({
        method: 'GET',
        apiPath: `/bouldern/gym-map-resources/?name=${gymName.value}`,
      }).then((response) => {
        gym.value = response.data['gym'];
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

          // set style according to activeness
          if (isActiveGrade(boulder.grade)) {
            resetBoulderStyle(boulder);
          } else {
            boulder.setStyle(invisible);
          }

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
          if (onMapLoaded) onMapLoaded();
        };
        mapImage.src = gym.value.map;
      });
      favorite.value = store.state.favoriteGyms.includes(gymName.value);
    }

    const loaded = ref(false);

    // create popover

    const creating = ref(false);

    // selected boulder cannot be reactive because it breaks openlayers
    let selectedBoulder = {ascent: undefined};
    const selectedBoulderAge = ref(0);
    const selectedCoordinates = ref({});
    const selectedColor = ref(Colors.DEFAULT_COLOR);
    const selectedGradeColor = ref(Colors.DEFAULT_COLOR);
    const selectedGrade = computed(() => {
      return getGrade(selectedGradeColor.value.id);
    });

    /**
     * Opens the create popover and closes the old one if still open. Sets
     * selected coordinates to the event's feature's
     * coordinates and sets the drawn feature's style to the selected colors.
     *
     * @param event the draw event
     */
    async function openCreatePopover(event) {
      overlay.value.close();
      creating.value = true;
      await nextTick();
      const feature = event.feature;
      feature.ascent = null;
      const geometry = feature.getGeometry();

      selectedCoordinates.value = jsonFormat.value
          .writeGeometryObject(geometry);
      feature.setStyle(getBoulderStyle(
          selectedColor.value.color,
          getHexColor(selectedGrade.value.color),
          '0'));

      selectedBoulder = feature;
      overlay.value.open(geometry.getCoordinates());
    }

    // reset selected colors and close popover when changing gym
    watch(gymName, () => {
      selectedGradeColor.value = Colors.DEFAULT_COLOR;
      selectedColor.value = Colors.DEFAULT_COLOR;
      overlay.value.close();
    });

    /**
     * Sets the color style (hold and grade color) of the selected boulder
     *
     * @param holdColor the hold color to set
     * @param gradeColor the grade color to set
     */
    function setSelectedBoulderColorStyle(holdColor, gradeColor) {
      const style = selectedBoulder.getStyle();
      style[1] = getColorStyle(holdColor, gradeColor);
      selectedBoulder.setStyle(style);
    }

    /**
     * Adjusts the currently selected hold color when selecting a grade
     * and Updates both the hold and grade color of the most recently
     * added boulder to the provided event's color
     *
     * @param selectedOption the selected color Option
     */
    function updateGrade(selectedOption) {
      selectedGradeColor.value = selectedOption;
      setSelectedBoulderColorStyle(selectedOption.color, selectedOption.color);
    }

    /**
     * Updates the hold color of the most recently added boulder to the provided
     * event's color
     *
     * @param selectedOption the selected color Option
     */
    function updateHoldColor(selectedOption) {
      selectedColor.value = selectedOption;
      setSelectedBoulderColorStyle(
          selectedOption.color, getHexColor(selectedGrade.value.color));
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
     * Creates a new boulder via API call, sets the selected boulder's id to the
     * created one's and closes the create popover
     */
    function createBoulder() {
      const boulder = selectedBoulder;
      boulder.id = -1;
      boulder.grade = selectedGrade.value.id;
      boulder.color = selectedColor.value.id;
      boulder.age = 0;
      requestWithJwt({
        apiPath: `/bouldern/gym/${gym.value.id}/boulder/`,
        data: {
          coordinates: selectedCoordinates.value,
          color: selectedColor.value.id,
          grade: selectedGrade.value.id,
        },
      }).then((response) => {
        boulder.id = response.data.id;
      });
      overlay.value.close();
    }

    /**
     * Removes the popover's feature from the featureCollection
     */
    function onCloseCreatePopover() {
      if (selectedBoulder.id === undefined) {
        featureCollection.pop();
      }
      creating.value = false;
      selectedBoulder = null;
    }

    // Ascent popover
    const selectedAscentResult = ref(null);
    const reportingAscent = ref(false);

    const colorOptions = computed(() => store.state.colors);

    /**
     * Opens the ascent popover and closes the old one if still open.
     *
     * @param feature the clicked boulder
     */
    async function openAscentPopover(feature) {
      overlay.value.close();
      reportingAscent.value = true;
      await nextTick();
      selectedAscentResult.value = feature.ascent ?
          feature.ascent.result.toString() : null;
      selectedBoulder = feature;
      selectedBoulderAge.value = feature.age;

      selectedColor.value = colorOptions.value
          .filter((colorOption) => colorOption.id === feature.color)[0];
      selectedGradeColor.value = gradeColors.value
          .filter((colorOption) => colorOption.id === feature.grade)[0];

      overlay.value.open(feature.getGeometry().getCoordinates());
    }

    /**
     * Sets the ascent style of the selected boulder according to the currently
     * selected ascent status
     */
    function setAscentStyle() {
      const style = selectedBoulder.getStyle();
      style[2] = new Style({
        image: ascentIcons[selectedAscentResult.value],
      });
      selectedBoulder.setStyle(style);
    }

    /**
     * Submits the selected ascent result and closes the ascent popover.
     */
    function reportAscent() {
      const boulder = selectedBoulder;
      const ascent = {'result': selectedAscentResult.value};
      requestWithJwt({
        apiPath: `/bouldern/gym/${gym.value.id}/boulder/` +
            `${boulder.id}/ascent/`,
        data: ascent,
      });
      boulder.ascent = ascent;
      overlay.value.close();
    }

    const {t} = useI18n();
    // Selectable options for the result of an attempt to ascend a boulder.
    const ascentResults = [0, 1, 2].map((i) => t(`gymMap.ascentResults[${i}]`));

    /**
     * Sets the selected boulder inactive via an api call, removes it from the
     * feature collection, and closes the ascent popover
     */
    function retireBoulder() {
      requestWithJwt({
        apiPath: `/bouldern/gym/${gym.value.id}/boulder/` +
            `${selectedBoulder.id}/`,
        method: 'DELETE',
      });
      featureCollection.remove(featureCollection.getArray()
          .find((feature) => feature.id === selectedBoulder.id));
      overlay.value.close();
    }

    /**
     * Checks whether the specified boulder is currently being edited
     *
     * @param boulder the boulder to check
     * @returns {boolean} whether the boulder is being edited
     */
    function isBeingEdited(boulder) {
      return reportingAscent.value && boulder.id === selectedBoulder.id;
    }

    /**
     * Resets ascent status if it was changed.
     */
    function onCloseAscentPopover() {
      reportingAscent.value = false;
      if (selectedBoulder.ascent !== null) {
        if (selectedBoulder.ascent.result.toString() !==
            selectedAscentResult.value) {
          selectedAscentResult.value =
              selectedBoulder.ascent.result.toString();
          setAscentStyle();
        }
      } else {
        if (selectedAscentResult.value !== null) {
          selectedAscentResult.value = null;
          setAscentStyle();
        }
      }
      selectedBoulder = null;
    }

    // edit popover
    const editingBoulder = ref(false);

    // colors
    /**
     * Switches the popover content from ascent reporting to boulder editing
     */
    function openEditPopover() {
      reportingAscent.value = false;
      editingBoulder.value = true;
    }

    /**
     * If changes made to boulder were not saved, reverts them and closes the
     * edit popover.
     */
    function onCloseEditPopover() {
      if (selectedBoulder.grade !== selectedGradeColor.value.id ||
          selectedBoulder.color !== selectedColor.value.id) {
        resetBoulderStyle(selectedBoulder);
      }
      editingBoulder.value = false;
      selectedGradeColor.value = Colors.DEFAULT_COLOR;
      selectedColor.value = Colors.DEFAULT_COLOR;
    }

    /**
     * Creates a new boulder via API call, sets the selected boulder's id to the
     * created one's and closes the create popover
     */
    function editSelectedBoulder() {
      const boulder = selectedBoulder;
      boulder.grade = selectedGrade.value.id;
      boulder.color = selectedColor.value.id;
      updateBoulder(boulder, (({color, grade}) => ({color, grade}))(boulder));
      overlay.value.close();
    }


    /**
     * Creates the selected boulder if in create mode, or updates it when in
     * edit mode
     */
    function createOrUpdateBoulder() {
      if (creating.value) {
        createBoulder();
      } else if (editingBoulder.value) {
        editSelectedBoulder();
      }
    }

    /**
     * calls close popover handler for create / ascent popover
     */
    function onClosePopover() {
      if (creating.value) {
        onCloseCreatePopover();
      } else if (reportingAscent.value) {
        onCloseAscentPopover();
      } else if (editingBoulder.value) {
        onCloseEditPopover();
      }
    }

    // filtering by grade

    const filtering = ref(false);

    const allGradesActive = ref(true);

    /**
     * Sets all grades active / inactive when toggling "all" checkbox
     */
    function selectGrades(allGradesActive) {
      if (allGradesActive) {
        setAllGradesActive();
      } else {
        activeGrades.value = [];
      }
    }

    const activeGrades = ref([]);

    // set boulders of filtered grades invisible and those of active grades
    // visible
    watch(activeGrades, () => {
      featureCollection.forEach((boulder) => {
        // if boulder's grade is active and boulder is invisible, show it
        if (isActiveGrade(boulder.grade)) {
          if (boulder.getStyle() === invisible) {
            resetBoulderStyle(boulder);
          }
          // if boulder's grade is inactive and boulder is visible, hide it
        } else {
          if (boulder.getStyle() !== invisible) {
            boulder.setStyle(invisible);
          }
        }
      });
    });

    /**
     * Adds all the gym's grades to the set of active grades
     */
    function setAllGradesActive() {
      allGradesActive.value = true;
      activeGrades.value = gym.value.grade_set.map(({id}) => id);
    }

    /**
     * Checks whether the grade with the specified id is active
     *
     * @param gradeId id of the grade to check whether it's active
     * @returns {boolean} whether the grade is active or not
     */
    function isActiveGrade(gradeId) {
      return activeGrades.value.includes(gradeId);
    }

    // loading gym map
    const grabbingBoulder = ref(false);
    let timer;

    /**
     * Gets the time that has passed since the provided timestamp
     *
     * @param timeStamp timestamp to get the delay for, has to be same unit as
     * performance.now()
     * @returns {number} time that has passed since the provided timestamp in
     * milliseconds
     */
    function getDelay(timeStamp) {
      return performance.now() - timeStamp;
    }

    /**
     * Gets the time that has passed since the provided event
     *
     * @param event openlayers map event to get the delay for
     * @returns {number} time that has passed since the provided event in
     * milliseconds
     */
    function getEventDelay(event) {
      return getDelay(event.originalEvent.timeStamp);
    }

    /**
     * Sets the cursor's style on the map to the provided one
     */
    function setCursorStyle(style) {
      map.getViewport().style.cursor = style;
    }

    /**
     * Gets the boulder feature at the provided pixel. Ignores invisible
     * boulders
     *
     * @param pixel pixel at which to look for a boulder
     * @returns {undefined | object} the boulder feature at the provided pixel
     * if there is one, undefined otherwise
     */
    function getBoulderAtPixel(pixel) {
      const boulder = map
          .forEachFeatureAtPixel(pixel, (feature) => feature);
      if (boulder &&
          boulder.getStyle() !== invisible &&
          boulder.id !== undefined) {
        return boulder;
      }
      return undefined;
    }

    /**
     * Sets the radius of the provided boulder's color style to the provided
     * value
     */
    function setBoulderRadius(boulder, radius) {
      const style = boulder.getStyle();
      const colorStyle = style[1].getImage();
      colorStyle.setRadius(radius);
      style[1].setImage(colorStyle);
      boulder.setStyle(style);
    }

    const clickStart = ref(NaN);
    const modifyRadius = 35;

    /**
     * Updates the provided boulder with the provided data via boulder api
     *
     * @param boulder the boulder for which to send the update
     * @param data boulder properties to update
     */
    function updateBoulder(boulder, data) {
      requestWithJwt({
        apiPath: `/bouldern/gym/${gym.value.id}/boulder/${boulder.id}/`,
        method: 'PATCH',
        data: data,
      });
    }

    /**
     * Sets the loaded flag and initializes the map
     */
    function onGymMapLoaded() {
      setAllGradesActive();

      // draw interaction
      drawInteraction.on('drawend', openCreatePopover);
      map.addInteraction(drawInteraction);

      // modify interaction
      map.addInteraction(dragPanInteraction);
      let initialBoulderCoordinates;
      modifyInteraction.on('modifystart', (event) => {
        initialBoulderCoordinates = event.features.getArray()[0]
            .getGeometry().getCoordinates();
        // deactivate drag pan
        setCursorStyle('grabbing');
        dragPanInteraction.setActive(false);
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
          updateBoulder(boulder, {
            coordinates: jsonFormat.value.writeGeometryObject(boulderGeometry),
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
        if (boulder && !isBeingEdited(boulder)) {
          if (event.originalEvent.pointerType === 'touch') {
            timer = setTimeout(() => {
              // fire event only once and only if not panning the map
              if (getEventDelay(event) < 2 * modifyTouchThreshold &&
                      !moving.value) {
                setBoulderRadius(boulder, modifyRadius);
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

      // handler for opening ascent popover or resetting a boulder's style
      // after moving
      map.on('click', (event) => {
        const boulder = getBoulderAtPixel(event.pixel);
        if (boulder) {
          if (getDelay(clickStart.value) >= modifyTouchThreshold) {
            setBoulderRadius(boulder, boulderRadius);
          } else {
            openAscentPopover(boulder);
          }
        }
      });

      // cursor style
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
      if (newGymName !== null && newGymName !== undefined) {
        featureCollection.clear();
        loadGymMap(setAllGradesActive);
        appView.value.collapseDrawer();
      }
    });

    /**
     * Creates/removes a favorite gym entry for thfis gym
     */
    function setFavorite() {
      favorite.value = !favorite.value;
      if (favorite.value) {
        store.dispatch('addFavoriteGym', gymName.value);
      } else {
        store.dispatch('removeFavoriteGym', gymName.value);
      }
    }

    // edit gym view

    const gymForm = ref(null);
    const editingGym = ref(false);

    /**
     * Opens the edit gym view
     */
    function editGym() {
      menu.value = false;
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
            resetBoulderStyle(boulder);
          } else {
            vectorSource.removeFeature(boulder);
          }
        });
        editingGym.value = false;
      });
    }

    const appView = ref(null);

    /**
     * Refreshes the gym map
     */
    function refresh() {
      featureCollection.clear();
      loadGymMap();
      appView.value.collapseDrawer();
    }

    const menu = ref(false);
    const deleteDialog = ref(false);

    /**
     * Opens the gym deletion dialog
     */
    function openDeleteDialog() {
      menu.value = false;
      deleteDialog.value = true;
    }

    const router = useRouter();

    /**
     * Calls the gym deletion action and redirects to home view
     */
    function deleteGym() {
      store.dispatch('deleteGym', gym.value);
      gym.value = defaultGym;
      router.push('/');
    }

    const menuItems = computed(() => {
      const items = [
        {
          title: t('gymMap.edit'),
          callback: editGym,
        },
      ];
      if (store.state.user.id === gym.value.created_by) {
        items.push({
          title: t('gymMap.deleteGym'),
          callback: openDeleteDialog,
        });
      }
      return items;
    });

    return {
      // colors
      getHexColor,
      // gym map
      gym,
      ascentResults,
      mapRoot,
      loaded,
      overlay,
      creating,
      reportingAscent,
      // create popover
      selectedCoordinates,
      selectedColor,
      gradeColors,
      selectedGradeColor,
      updateGrade,
      updateHoldColor,
      createOrUpdateBoulder,
      // ascent popover
      selectedBoulder,
      selectedBoulderAge,
      selectedAscentResult,
      setAscentStyle,
      retireBoulder,
      reportAscent,
      onClosePopover,
      // ascent popover
      editingBoulder,
      openEditPopover,
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
      // refresh button
      appView,
      refresh,
      // expose map to cypress
      map,
      getBoulderAtPixel,
      boulderRadius,
      modifyRadius,
      // menu
      menu,
      menuItems,
      deleteDialog,
      deleteGym,
    };
  },
};
</script>

<style>
@import '../../node_modules/ol/ol.css';

#id_map-root {
  width: 100%;
  height: 100%;
}
</style>
