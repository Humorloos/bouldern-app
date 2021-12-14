<template>
  <div id="difficulty-level">
    <slot />
    <input
      :id="colorFieldId"
      type="hidden"
      :name="colorFieldName"
      :value="activeColor.value"
    >
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
  name: 'DifficultyLevelSelect',
  components: {
    vSelect,
  },
  props: {
    options: {
      type: Object,
      default: function() {
        return {};
      },
    },
    prefix: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      activeColor: {
        label: '',
        style: {color: 'white'},
        value: -1,
      },
    };
  },
  computed: {
    colorFieldName() {
      return this.prefix + '-color';
    },
    colorFieldId() {
      return 'id_' + this.colorFieldName;
    },
  },
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
