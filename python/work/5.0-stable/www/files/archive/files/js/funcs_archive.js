/*** выделение элемента при наведении ***/
function overElem(elem, over_class) {
	var cur_class = "";
	if (elem.className) {
		cur_class = rtrim(elem.className);
	}
	if (over_class) {
		elem.className = cur_class + " " + over_class;
	} else {
		elem.className = cur_class + " act";
	}
}
function outElem(elem, over_class) {
	var cur_class = elem.className;
	if (cur_class) {
		if (cur_class.indexOf(over_class) > -1) {
			elem.className = cur_class.substr(0, cur_class.indexOf(over_class)-1);
		}
	}
}

/*** информация за день ***/
/*function showTitleInfoDay(elem, param) {
	var content = '<div><span>Всего источников:</span> '+param.source+'</div>';
	content += '<div><span>Всего видеороликов:</span> '+param.video+'</div>';
	//content += '<div><span>Найдено лиц:</span>'+param.faces+'</div>';
	//content += '<div><span>Найдено людей:</span>'+param.persons+'</div>';
	createTitleWindow({distX: 5, width: 180, elem: elem, id: 'win_infoDay', txt: content});
}
*/
/*** информация о видеоролике ***/
/*function showTitleVideo(elem, param) {
	var content = '<div><span>Формат:</span> '+param.format+'</div>';
	content += '<div><span>Размер:</span> '+param.size+'</div>';
	content += '<div><span>Сигнал:</span> '+param.signal+'</div>';
	content += '<div><span>Частота кадров:</span> '+param.fps+'</div>';
	content += '<div><span>Найдено лиц:</span> '+param.faces+'</div>';
	content += '<div><span>Найдено людей:</span> '+param.persons+'</div>';
	createTitleWindow({distX: 5, width: 230, elem: elem, id: 'win_video', txt: content});
}
function showMenuVideo(elem, face, people, id_roller) {
    document.getElementById('sourseid').innerHTML = id_roller; 
	var content = '<ul><li><a href="/page_view_video/'+id_roller+'/">Просмотр</a></li>';
	content += '<li><a href="page_video_faces.html">Найденные лица ('+face+')</a></li>';
	content += '<li><a href="page_video_persons.html">Найденные люди ('+people+')</a></li></ul>';
	createInfoWindow({distX: 5, width: 250, height: 150, elem: elem, id: 'win_videoMenu', txt: content});
}
*/
/*** выделить все элементы на странице ***/
function checkAllRow(id, count) {
	var inp = byId(id);
	if (inp.id == 'choose_all') {
		byId('choose_all2').checked = inp.checked;
	} else {
		byId('choose_all').checked = inp.checked;
	}
	var check;
	for (var i = 1; i <= count; i++) {
		check = byId('check'+i);
		if (inp.checked) {		
			check.checked = true;
		} else {		
			check.checked = false;
		}
	}
}
function checkAll(elem, count) {
	var inp = byId(elem);
	if (inp.id == 'choose_all') {
		byId('choose_all2').checked = inp.checked;
	} else {
		byId('choose_all').checked = inp.checked;
	}
	var check;
	for (var i = 1; i <= count; i++) {
		check = byId('check'+i);
		if (inp.checked) {		
			check.checked = 'checked';
			searchElem(check, 'LI').className = 'act';
		} else {		
			check.checked = false;
			searchElem(check, 'LI').className = '';
		}
	}
}
function searchElem(el, nameNode) {
	var parentObj = el;
	var parentName = parentObj.nodeName;
	while (parentName != nameNode) {
		parentObj = parentObj.parentNode;
		parentName = parentObj.nodeName;
	}	
	return parentObj;
}
function isChecked(count) {
	var c = 0;
	if (count > 0) {
		while (count > 0) {
			if (byId("check"+count)) {
				if (byId("check"+count).checked) {
					c++;
				}
			}
			count--;
		}
	}
	return c;
}
/*** удаление, обучение, экспорт фотографий ***/
function showMessageDelete(count, name_block) {
	var txt;
	var head;
	var check = isChecked(count);
	if (check) {
		txt = createTextMessage({name_block: name_block+"_del", count: check});
		changeWindow({id: 'win_del', css: {width: '300px', height: '200px'}, txt: txt});
	} else {
		txt = createTextMessage({name_block: name_block});
		changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: txt});
	}
}
function showMessageLearn(count, name_block) {
	var txt;
	var head;
	var check = isChecked(count);
	if (check) {
		txt = createTextMessage({name_block: name_block+"_learn", count: check});
		changeWindow({id: 'win_learn', css: {width: '300px', height: '200px'}, txt: txt});
	} else {
		txt = createTextMessage({name_block: name_block});
		changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: txt});
	}
}
function showMessageExport(count, name_block) {
	var txt;
	var head;
	var check = isChecked(count);
	if (check) {
		/*txt = createTextMessage({name_block: name_block+"_export", count: check});*/
		changeWindow({id: 'win_export', css: {width: '300px', height: '200px'}});
		//alert('yes');
	} else {
		txt = createTextMessage({name_block: name_block});
		changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: txt});
	}
}
function saveArchive(ok, desc) {
	closeChangeWindow('win_export');
	var txt_beg = 'Скачать архив с фотографиями';
	var head = 'Экспорт фотографий';
	if (desc) {
		txt_beg='Скачать архив с видеороликами';
		head = 'Экспорт видеороликов';
	} 
	var txt=txt_beg+' вы можете <div class="linkArchive"><a href="#">здесь</a></div>';
	if (ok) {
		changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: txt, head: head});
	}
}
function showTimeLine() {
	closeChangeWindow('win_export');
	changeWindow({id: 'win_progressbar', css: {width: '300px', height: '200px'}});
	runit();
}
/*** всплывающие подсказки ***/
function getTextTitle(id) {
	switch (id) {
		case "title_time_source": 
			return 'Формат времени:<div>часы : минуты : секунды</div>';
			break;
		default: 
			return 'Всплывающая подсказка';
			break;				
	}
}
function showTitleForm(elem) {
	var content = getTextTitle(elem.id);
	createTitleWindow({distX: 5, width: 230, elem: elem, id: 'title', txt: content});
}