<template>
  <div id="difficulty-level">
    <v-select
      v-model="value"
      :options="options"
      :searchable="false"
      :clearable="false"
    >
      <template #option="option">
        <span :style="option.style">{{ option.label }}</span>
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
        return {
          style: {color: color.color},
          label: color.name,
        };
      });
    },
    value: {
      get() {
        return {
          style: {
            color: this.modelValue.color,
          },
          label: this.modelValue.name,
        };
      },
      set(value) {
        this.$emit('update:modelValue', {
          color: value.style.color,
          name: value.label,
        });
      },
    },
  },
};
</script>

<style>
/*noinspection CssUnusedSymbol*/
.vs__selected::before {
  /*noinspection CssInvalidFunction*/
  background-color: v-bind("value.style.color");
  border-radius: 50%;
  content: " ";
  display: flex;
  margin-right: 8px;
  height: 10px;
  width: 10px;
}
</style>
