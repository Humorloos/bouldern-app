'use strict';

$(document).ready(function () {
    const $difficultyLevelSelect = $('select');
    this.setDifficultyLevelBackgroundColor = function () {
        this.style.backgroundColor = this.options[this.value].style.backgroundColor
    };
    $difficultyLevelSelect.change(this.setDifficultyLevelBackgroundColor)

    $('#add-level-button').click(this, function(event) {
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
})