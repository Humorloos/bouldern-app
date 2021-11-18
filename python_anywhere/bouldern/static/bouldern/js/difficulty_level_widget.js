$(document).ready(function () {
    $('select').each(function () {
        const $difficultyLevelSelect = $(this);
        $difficultyLevelSelect.change(() => {
            $difficultyLevelSelect[0].style.backgroundColor =
                $difficultyLevelSelect[0].options[$difficultyLevelSelect.val()].style.backgroundColor
        })
    })
})