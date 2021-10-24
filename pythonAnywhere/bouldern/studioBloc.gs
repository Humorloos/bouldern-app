// noinspection JSUnresolvedVariable,JSUnresolvedFunction,JSUnusedGlobalSymbols

function imageUpdate() {
    const oNow = new Date();
    const oFiveMinutesBeforeNow = new Date(oNow.getTime() - (5 * 60 * 1000));
    const oOneHourFromNow = new Date(oNow.getTime() + (60 * 60 * 1000));

    const oTriggeringEvent = CalendarApp.getEvents(oFiveMinutesBeforeNow, oOneHourFromNow).pop();
    const sEventTitle = oTriggeringEvent.getTitle();
    const sFormId = oTriggeringEvent.getDescription();
    const oTargetForm = FormApp.openById(sFormId);
    const oImageItems = oTargetForm.getItems(FormApp.ItemType.IMAGE);
    if (sEventTitle === 'Bouldern Form Update') {
        oImageItems.slice(1).forEach(item => {
            const sImageName = `${item.getTitle().match('Wand (.*)')[1]}.png`;
            const oNewImage = DriveApp.getFilesByName(sImageName).next().getBlob();
            item.asImageItem().setImage(oNewImage);
        });
    } else if (sEventTitle === 'Bouldern Progress Update') {
        const sGymName = oTargetForm.getTitle().toLowerCase().replace(' ', '_');
        const oNewImage = UrlFetchApp.fetch(`https://humorloos.pythonanywhere.com/bouldern/${sGymName}.png`)
            .getAs('image/png');
        oImageItems[1].asImageItem().setImage(oNewImage);
    }
}

function studioBlocOnSubmit() {
    UrlFetchApp.fetch("https://humorloos.pythonanywhere.com/studio_bloc/", {"method": "post"});
}
