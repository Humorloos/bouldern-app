<template>
  <div
    id="popup"
    ref="popup"
    class="ol-popup"
    :style="{visibility: loaded ? 'visible' : 'hidden'}"
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
    <vue-form
      :api-path="`/bouldern/gym/${mapData.id}/boulder/`"
      :form="mapData.boulder_set.at(-1)"
      @submitted="onSubmitted"
    />
  </div>
  <div
    id="map-root"
    ref="map-root"
  />
</template>

<script>
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
import VueForm from '@/components/VueForm';

export default {
  name: 'GymMapView',
  components: {
    VueForm,
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
      mapImage: new Image(),
      jsonFormat: new GeoJSON(),
      selectedCoordinate: 'none yet',
      loaded: false,
    };
  },
  computed: {
    ...mapState([
      'authToken',
    ]),
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
        self.mapData.boulder_set.push({
          coordinates: self.jsonFormat
              .writeGeometryObject(event.element.getGeometry()),
        });
        self.popover['feature'] = event.element;
      });
      return featureCollection;
    },
    extent() {
      return [0, 0, this.mapImage.width, this.mapImage.height];
    },
    projection() {
      return new Projection({
        code: 'xkcd-image',
        units: 'pixels',
        extent: this.extent,
      });
    },
    source() {
      const source = new VectorSource({
        features: this.featureCollection,
        useSpatialIndex: false, // improves performance
      });
      // Populate with initial features
      this.mapData.boulder_set.forEach(
          (boulder) => source.addFeature(
              this.jsonFormat.readFeature(boulder.coordinates)));
      return source;
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
  created() {
    this.axios.get(`/bouldern/gym/?name=${this.$route.params.gymName}`, {
      headers: {
        'authorization': `Bearer ${this.authToken.token}`,
      },
    }).then((response) => {
      this.mapData = response.data[0];
      this.mapImage.src = this.mapData.map;
      this.mapImage.onload = () => {
        this.map;
        this.loaded = true;
      };
    });
  },
  mounted() {
    if (window.Cypress) {
      window[this.$options.name] = this;
    }
  },
  methods: {
    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
    closePopover() {
      this.featureCollection.remove(this.popover.feature);
      this.popover.setPosition(undefined);
      return false;
    },
    onSubmitted() {
      this.popover.setPosition(undefined);
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
  top: 2px;
  right: 8px;
}

.ol-popup-closer:after {
  content: "✖";
}
</style>
