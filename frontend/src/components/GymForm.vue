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
</template>

<script>
import $ from "jquery";

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
}
</script>
