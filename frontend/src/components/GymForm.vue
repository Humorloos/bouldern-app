<template>
  <form action="/bouldern/add-gym/" method="post" enctype="multipart/form-data">
    <slot name="gym-form"></slot>
    <h3>Difficulty Levels</h3>
    <div id="difficulty-levels">
      <slot name="difficulty-levels"></slot>
    </div>
    <button type="button" id="add-level-button">Add Level</button>
    <input type="submit" value="Submit">
  </form>
  <v-select :options="options" :searchable="false">
    <template #option="option">
      <span :style="option.style">{{ option.label }}</span>
    </template>
  </v-select>
</template>

<script>
import $ from "jquery";
import vSelect from "vue-select"

$(document).ready(function () {
  const $difficultyLevelSelect = $('select');
  this.setDifficultyLevelBackgroundColor = function () {
    this.style.backgroundColor = this.options[this.value].style.backgroundColor
  };
  $difficultyLevelSelect.change(this.setDifficultyLevelBackgroundColor)

  $('#add-level-button').click(this, function (event) {
    const level = $('#difficulty-levels div').length
    const $difficultyLevel = $('#difficulty-level').first().clone()

    const attributesToReplace = ['for', 'name', 'id']
    attributesToReplace.forEach(attribute => {
      $difficultyLevel.children().each(function () {
        const oldAttribute = this.getAttribute(attribute);
        if (oldAttribute !== null) {
          this.setAttribute(attribute,
              oldAttribute.replace('difficultylevel_set-0', 'difficultylevel_set-' + level))
        }
      })
    })

    $difficultyLevel.find('[name$="level"]')[0].value = level
    $difficultyLevel.find('select').change(event.data.setDifficultyLevelBackgroundColor)
    $('#difficulty-levels').append($difficultyLevel);

    $('[name$="TOTAL_FORMS"]')[0].value = level + 1
  })
});
export default {
  name: "gym-form",
  components: {
    vSelect
  },
  data: function () {
    return {
      options: [
        {
          label: 'Promos',
          style: {'color': 'purple'}
        },
        {
          label: 'Adverts',
          style: {'color': 'purple'}
        },
        {
          label: 'Others',
          style: {'color': 'purple'}
        },
        {
          label: 'Custom',
          style: {'color': 'yellow'}
        },
      ]
    }
  }
}
</script>

<style>
.vs__selected::before {
  background-color: purple;
  border-radius: 50%;
  content: " ";
  display: flex;
  margin-right: 8px;
  height: 10px;
  width: 10px;
}
</style>
