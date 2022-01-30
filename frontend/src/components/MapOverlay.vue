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
      @click="close"
    />
    <v-container
      id="popup-content"
    >
      <slot name="content" />
    </v-container>
  </div>
</template>

<script>
/** @file todo */

import {Overlay} from 'ol';


export default {
  name: 'MapOverlay',
  props: {
    loaded: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['close'],
  computed: {
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
  },
  methods: {
    /**
     * todo
     */
    close() {
      if (this.popover.getPosition() !== undefined) {
        this.$emit('close');
        this.popover.setPosition(undefined);
      }
    },
    /**
     * todo
     */
    open(coordinates) {
      if (this.popover.getPosition() !== undefined) {
        this.close();
      }
      this.popover.setPosition(coordinates);
    },
  },
};
</script>

<style scoped>

.ol-popup {
  position: absolute;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #cccccc;
  bottom: 12px;
  left: -50px;
  min-width: 320px;
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
