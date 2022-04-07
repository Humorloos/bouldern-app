<template>
  <v-row>
    <v-col>
      {{ $t('boulderForm.grade') }}
      <color-select
        id="id_grade-select"
        v-model="gradeColorValue"
        :color-options="gradeColorOptions"
        @update:model-value="onUpdateGradeColor($event)"
      />
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      {{ $t('boulderForm.holdColor') }}
      <color-select
        id="id_color-select"
        v-model="holdColorValue"
        :color-options="holdColorOptions"
        @update:model-value="$emit('update:holdColor', $event)"
      />
    </v-col>
  </v-row>
  <v-btn
    id="id_save-boulder"
    @click="$emit('save')"
  >
    {{ $t('boulderForm.lblSave') }}
  </v-btn>
</template>

<script>
/** @file form for creating and editing boulders */
import {Colors} from '../constants/color.js';
import ColorSelect from './ColorSelect.vue';
import {computed, ref} from 'vue';
import {useStore} from 'vuex';

export default {
  name: 'BoulderForm',
  components: {
    ColorSelect,
  },
  props: {
    holdColor: {
      type: Object,
      default: () => Colors.DEFAULT_COLOR,
    },
    gradeColor: {
      type: Object,
      default: () => Colors.DEFAULT_COLOR,
    },
    gradeColorOptions: {
      type: Array,
      default: () => [],
    },
  },
  emits: ['update:holdColor', 'update:gradeColor', 'save'],
  setup(props, {emit}) {
    const store = useStore();
    const holdColorOptions = computed(() => store.state.colors);
    const holdColorValue = ref(props.holdColor);
    const gradeColorValue = ref(props.gradeColor);

    /**
     * Sets hold color to selected grade color and emits update event for both
     * hold and grade color
     */
    function onUpdateGradeColor(event) {
      emit('update:gradeColor', event);
      holdColorValue.value = holdColorOptions.value.filter(
          (colorOption) => colorOption.color === event.color)[0];
      emit('update:holdColor', holdColorValue.value);
    }

    return {
      holdColorValue,
      gradeColorValue,
      holdColorOptions,
      onUpdateGradeColor,
    };
  },
};
</script>

<style scoped>

</style>
