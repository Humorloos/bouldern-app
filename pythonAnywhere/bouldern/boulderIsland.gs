// noinspection JSUnresolvedVariable

function boulderIslandOnSubmit() {
    UrlFetchApp.fetch("https://humorloos.pythonanywhere.com/boulder_island/", {"method": "post"});
}