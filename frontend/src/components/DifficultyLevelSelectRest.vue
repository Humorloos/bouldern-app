<template>
  <div id="difficulty-level">
    <v-select
      v-model="value"
      :options="options"
      :searchable="false"
      :clearable="false"
    >
      <template #option="option">
        <span :style="`color: ${option.color}`">
          {{ option.label }}
        </span>
      </template>
    </v-select>
  </div>
</template>

<script>
import vSelect from 'vue-select';

export default {
  name: 'DifficultyLevelSelectRest',
  components: {
    vSelect,
  },
  props: {
    colors: {
      type: Array,
      default: function() {
        return [];
      },
    },
    modelValue: {
      type: Object,
      default: () => {
      },
    },
  },
  emits: ['update:modelValue'],
  computed: {
    options() {
      return this.colors.map((color) => {
        return this.optionFromColor(color);
      });
    },
    value: {
      get() {
        return this.optionFromColor(this.modelValue);
      },
      set(value) {
        this.$emit('update:modelValue', {
          color: value.color,
          name: value.label,
        });
      },
    },
  },
  methods: {
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
