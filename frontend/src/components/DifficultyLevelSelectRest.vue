<template>
  <div id="difficulty-level">
    <v-select
      v-model="activeColor"
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
        return {
          level: 0,
          color: 0,
          label: '',
        };
      },
    },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      activeColor: {
        style: {color: 'white'},
        label: '',
      },
    };
  },
  computed: {
    options() {
      return this.colors.map((color) => {
        return {
          style: {color: color.color},
          label: color.name,
        };
      });
    },
    // value: {
    //   get() {
    //     return this.modelValue;
    //   },
    //   set(value) {
    //     this.$emit('update:modelValue', this.modelValue);
    //   },
    // },
  },
  // methods: {
  //   onInput(event) {
  //     this.$emit('update:model-value', this.modelValue);
  //   },
  // },
};
</script>

<style>
/*noinspection CssUnusedSymbol*/
.vs__selected::before {
  /*noinspection CssInvalidFunction*/
  background-color: v-bind("activeColor.style.color");
  border-radius: 50%;
  content: " ";
  display: flex;
  margin-right: 8px;
  height: 10px;
  width: 10px;
}
</style>
