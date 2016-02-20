function blockUser(elem, _class, count) {
    var login = byId('user'+count).innerHTML;
    if (elem.className.indexOf(_class) > - 1) {
        outElem(byId('row'+count), 'block');
        outElem(elem, _class);
        var content = BLOCK_USER + ' "'+login+'"';
    } else {
        //byId('row'+count).className = byId('row'+count).className + ' block';
        overElem(byId('row'+count), 'block');
        overElem(elem, _class);
        var content = USER + ' "'+login+'" ' + BLOCK;
    }
    createTitleWindow({distX: 5, width: 100, elem: elem, id: 'win_info', txt: content});
}
function showTitle(elem, count) {
    var login = byId('user'+count).innerHTML;
    if (elem.className.indexOf('act') > - 1) {
        var content = USER + ' "'+login+'" ' + BLOCK;
    } else {
        var content = BLOCK_USER + ' "'+login+'"';
    }
    createTitleWindow({distX: 5, width: 100, elem: elem, id: 'win_info', txt: content});
}