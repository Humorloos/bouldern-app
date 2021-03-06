<template>
  <div>
    <vue-select
      v-model="value"
      :options="options"
      :searchable="false"
      :clearable="false"
      :disabled="disabled"
    >
      <template #option="option">
        <span :style="`color: ${option.color}`">
          {{ option.label }}
        </span>
      </template>
    </vue-select>
  </div>
</template>

<script>
/** @file select field for color of a grade */

import vSelect from 'vue-select';

export default {
  name: 'ColorSelect',
  components: {
    vueSelect: vSelect,
  },
  props: {
    colorOptions: {
      type: Array,
      default: () => [],
    },
    modelValue: {
      type: Object,
      default: () => {},
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue'],
  computed: {
    /**
     * Gets grade select options (which require label property) for
     * color options.
     *
     * @returns {object[]} array of grade select options
     */
    options() {
      return this.colorOptions.map((color) => {
        return this.optionFromColor(color);
      });
    },
    /**
     * Value property is computed with get() and set() for allowing usage with
     * v-model
     */
    value: {
      get() {
        return this.optionFromColor(this.modelValue);
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
  },
  methods: {
    /**
     * Converts a color object (as returned by color api) into a vue-select
     * option (requires changing property name to label)
     *
     * @param color the color to convert
     * @returns {object} the vue-select option
     */
    optionFromColor(color) {
      return {
        ...color,
        label: color.name,
      };
    },
  },
};
</script>

<style>
@import '../../node_modules/vue-select/dist/vue-select.css';
/*noinspection CssUnusedSymbol*/
.vs__selected::before {
  /*noinspection CssInvalidFunction*/
  background-color: v-bind("value.color");
  border-radius: 50%;
  content: " ";
  display: flex;
  margin-right: 8px;
  height: 10px;
  width: 10px;
}
</style>
