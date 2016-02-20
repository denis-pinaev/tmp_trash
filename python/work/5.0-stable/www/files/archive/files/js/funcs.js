function flashVersion() {
   // Отдельно определяем Internet Explorer
   var ua = navigator.userAgent.toLowerCase();
   var isIE = (ua.indexOf("msie") != -1 && ua.indexOf("opera") == -1 && ua.indexOf("webtv") == -1);
   // Стартовые переменные
   var version = 0;
   var lastVersion = 20; // c запасом
   var i;
   if (isIE) { // browser == IE
       try {
           for (i = 3; i <= lastVersion; i++) {
               if (eval('new ActiveXObject("ShockwaveFlash.ShockwaveFlash.'+i+'")')) {
                  version = i;
               }
           }
       } catch(e) {}
   }
   else { // browser != IE
     for (i = 0; i < navigator.plugins.length; i++) {
         if (navigator.plugins[i].name.indexOf('Flash') != -1) {
            var flash = navigator.plugins[i];
            if (flash.version) {
                version = parseFloat(flash.version)
            } else {
                var strLength = flash.description.length;
                version = parseFloat(flash.description.substring(15, flash.description.indexOf('r')));            
            }
         }
     }
   }
   if (version >= 10) { return true; } 
   else { return false; }
}

function readCookie(name) {
   var nameEQ = name + "=";
   var ca = document.cookie.split(';');
   for(var i=0;i < ca.length;i++) {
       var c = ca[i];
       while (c.charAt(0)==' ') c = c.substring(1,c.length);
       if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
   }
   return null;
}

﻿function buttonStatus(btn, status) {
	var w = btn.offsetWidth;
	var h = btn.offsetHeight;
	var path = '/files/images/button'+w+'x'+h+'_'+status+'.gif';
	btn.style.backgroundImage = "url("+path+")";
}
function linkStatus(link, status, p) {
	var path = '/files/images/button'+p+'x24_'+status+'.gif';
	link.style.backgroundImage = "url("+path+")";
}

function byId(node) {
	return typeof node == 'string' ? document.getElementById(node) : node;
}

function checkPhoto(obj, count) {
	var inp = byId(obj);
	var li = searchElem(inp, 'LI');
	if (inp.checked) {
		li.className = 'act';
		checkAllElem(count);
	} else {
		li.className = '';
		byId('choose_all').checked = false;
		if (byId('choose_all2')) {
			byId('choose_all2').checked = false;
		}		
	}
}

function checkAllElem(count) {
	var count_checked = 0;
	for (var i = 1; i <= count; i++) {
	    if (byId('check'+i)){
		if (byId('check'+i).checked) {
			count_checked++;
		}
	    }
	}
	if (count == count_checked) {
		document.getElementById('choose_all').checked = true;
		if (document.getElementById('choose_all2')) {
			document.getElementById('choose_all2').checked = true;
		}	
	}	
}

function createTextMessage(param) {
	switch (param.name_block) {
		case "persons": 
			return 'Выберите, пожалуйста, хотя бы одну персону.';
			break;
		case "person": 
			return 'Выберите, пожалуйста, хотя бы одну фотографию персоны.';
			break;
		case "visitors": 
			return 'Выберите, пожалуйста, хотя бы одного посетителя.';
			break;
		case "staffs": 
			return 'Выберите, пожалуйста, хотя бы одного сотрудника.';
			break;
		case "photos": 
			return 'Выберите, пожалуйста, хотя бы одну фотографию.';
			break;
		case "users": 
			return 'Выберите, пожалуйста, хотя бы одного пользователя.';
			break;
		case "visitingcards": 
			return 'Выберите, пожалуйста, хотя бы одну карточку.';
			break;											
		case "operators": 
			return 'Выберите, пожалуйста, хотя бы одного оператора.';
			break;											
		case "video": 
			return 'Выберите, пожалуйста, хотя бы один видеоролик.';
			break;											
		case "persons_del": 
			return 'Вы, действительно, хотите удалить выбранных персон ('+param.count+' шт.)?';
			break;
		case "person_del": 
			return 'Вы, действительно, хотите удалить выбранные фотографии ('+param.count+' шт.)?';
			break;
		case "photos_del": 
			return 'Вы, действительно, хотите удалить выбранные фотографии ('+param.count+' шт.)?';
			break;
		case "operators_del": 
			return 'Вы, действительно, хотите удалить выбранныx операторов ('+param.count+' шт.)?';
			break;
		case "video_del": 
			return 'Вы, действительно, хотите удалить выбранное видео ('+param.count+' шт.)?';
			break;
		case "photos_export": 
			return 'Сохранить выделенные фотографии ('+param.count+' шт.)?';
			break;
		case "video_export": 
			return 'Сохранить выделенное видео ('+param.count+' шт.)?';
			break;
		case "photos_learn": 
			return 'Обучить выделенными фотографиями ('+param.count+' шт.)?';
			break;						
		case "visitors_del": 
			return 'Вы, действительно, хотите удалить выбранных посетителей ('+param.count+' шт.)?';
			break;
		case "staffs_del": 
			return 'Вы, действительно, хотите удалить выбранных сотрудников ('+param.count+' шт.)?';
			break;
		case "users_del": 
			return 'Вы, действительно, хотите удалить выбранных пользователей ('+param.count+' шт.)?';
			break;
		case "visitingcards_del": 
			return 'Вы, действительно, хотите удалить выбранные карточки ('+param.count+' шт.)?';
			break;										
		case "persons_zeroing": 
			return 'Вы, действительно, хотите удалить базу персон?';
			break;
		case "restart": 
			return 'Вы, действительно, хотите перезапустить систему?';
			break;
		case "reboot": 
			return 'Вы, действительно, хотите перезагрузить компьютер?';
			break;										
		default: 
			return 'Выберите, пожалуйста, хотя бы одно изображение.';
			break;
	}
}

function showMessage() {
	changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: 'Ошибка'});
}

function changeWindow(param) {
	if (param) {	
		if (param.id) {
			var win = byId(param.id);
		}
		if (param.css) {
			win.style.width = param.css.width;
			win.style.height = param.css.height;
		}
		if (param.txt) {		
			byId(param.id+'_contWF').innerHTML = param.txt;
		}
		if (param.head) {
			byId(param.id+'_headWF').innerHTML = param.head;
		}		
	}

	var scr = screenSize();	

	var t = win.style.top = (scr.h - parseInt(win.style.height))/ 2*0.8;
	if (t < 0) { t = 0 }
	t = t + 'px';
	win.style.left = (scr.w - parseInt(win.style.width)) / 2 + 'px';

	var browserType = navigator.userAgent.toLowerCase();
	if (browserType.indexOf('msie') >= 0) {
		win.style.position = 'absolute';
		win.style.top = parseInt(t)+ document.documentElement.scrollTop +'px';
		byId('block_fon').style.height = document.body.offsetHeight + 'px';
	} else {
		win.style.position = 'fixed';
	}

	win.style.display = 'block';
	byId('block_fon').style.display = 'block';
}

function closeChangeWindow(id) {
	if (byId(id)) {
		byId(id).style.display = 'none';
	}
	byId('block_fon').style.display = 'none';
}

function screenSize() {
	var w = '';
	var h = '';

	w = (window.innerWidth ? window.innerWidth : (document.documentElement.clientWidth ? document.documentElement.clientWidth : document.body.offsetWidth));
	h = (window.innerHeight ? window.innerHeight : (document.documentElement.clientHeight ? document.documentElement.clientHeight : document.body.offsetHeight));

	return { w: w, h: h };	
}

function showMessageZeroing(name_block) {
	var txt;
	txt = createTextMessage({name_block: name_block+'_zeroing'});
	changeWindow({id: 'win_zeroing', css: {width: '300px', height: '200px'}, txt: txt});
}

function rtrim(s) {
	return s.replace(/\s+$/, '');
}

function selectRow(tr, num) {
	var cur_class = "";
	if (tr.className) {
		cur_class = rtrim(tr.className);
	}
	var btn = byId("btn_play"+num);
	if (btn) {
		var btn_class = btn.className;
		btn.className = btn_class + "_act";
	}
	tr.className = cur_class + " act";
}

function unselectRow(tr, num) {
	if (tr.className.indexOf('odd') != -1) {
		tr.className = "odd";
	} else {
		tr.className = "";
	}
	var btn = byId("btn_play"+num);
	if (btn) {
		var btn_class = btn.className;
		var i = btn_class.indexOf('_act');;
		btn.className = btn_class.substr(0, i);
	}
}

function add_file(str, cl) {

	var inpContent = byId("tmp");
	var numEl = byId("load_img");

	if (!numEl) return false;

	var num = 0;
	if (numEl.innerText != undefined) {
		num = parseInt(numEl.innerText);   
	} else {
		num = parseInt(numEl.textContent);  
	}

	var inpArray = inpContent.getElementsByTagName('input');
	var lenArray = inpArray.length;

	var inpTemplate = byId("template_block");
	var inpOld = -1;
	var numFileInp = 0;

	for (var i = 0; i < lenArray; i++) {
		if ((inpArray[i].value == "") && (inpArray[i].type == 'file')) {
			if (inpOld == -1) {
				inpOld = i;
			} 
		}
		if (inpArray[i].type == 'file') {
			numFileInp++;
		}
	}
	if (str && (inpOld == -1) && (num <= 19)) {
		if (num < 19) {
			inpBlock = document.createElement("div");
			inpBlock.innerHTML = inpTemplate.innerHTML;
			if (cl) {
				inpBlock.className = cl;
			}
			inpContent.appendChild(inpBlock);

			newInpArr = inpBlock.getElementsByTagName('input');
			newInpArr[0].name = "template" + numFileInp;
		}
		num +=1;
	}	
	numEl.innerHTML = num;
}

function showBlock(id) {
	if (id.indexOf('radio1') != -1)  {
		byId(id).style.display='block'; 
		byId('radio2').style.display='none';
	} else {
		byId(id).style.display='block'; 
		byId('radio1').style.display='none';
	}
}

function searchChild(elem, nameNode, attrType) {
	var parent = byId(elem);
	var oChilds = parent.childNodes;
	for (var i = 0; i < oChilds.length; i++) {
		if (oChilds[i].nodeName == nameNode) {
			if (oChilds[i].getAttribute('TYPE') == attrType) {
				return oChilds[i];
			}
		}
	}
}

function checkPhoto2(el, num, count) {
	var li = searchElem(el, 'LI');
	var inp = byId('check'+num);
	if (inp.checked) {
		inp.checked = false;
		li.className = "";
		byId('choose_all').checked = false;
		if (byId('choose_all2')) {
			byId('choose_all2').checked = false;
		}		
	} else {
		inp.checked = true;
		li.className = "act";
		checkAllElem(count);
	}
}

function showLoupe(num, show) {
	byId('loupe'+num).style.display = show ? 'block' : 'none';
}

function test() {
	changeWindow({id: 'win_update', css: {width: '300px', height: '200px'}});
}

function getValueIsChecked(count) {
	var c = 0;
	var arr_value = new Array();
	if (count > 0) {
		while (count > 0) {
			if (byId("check"+count)) {
				if (byId("check"+count).checked) {
					arr_value[c] = byId("check"+count).value;
					c++;
				}
			}
			count--;
		}
	}
	return {c: c, array: arr_value};
}

function clickDelete(count) {
	closeChangeWindow('win_del');
	var obj = getValueIsChecked(count);
	for (var i = 0; i < obj.c; i++) {
		alert(obj.array[i]);
	}
}


function chooseCommunicator(objSel) {
	var active_value = '';
	var i = -1;
	var str1 = '';
	var str2 = '';
	if ( objSel.selectedIndex != -1)
	{
		active_value = objSel.options[objSel.selectedIndex].value;
		i = active_value.indexOf('_');
		if (i > -1) {
			str1 = active_value.substr(0, i);
			str2 = active_value.substr(i+1, active_value.length);
		}
	}
}

/* проверка на валидность данных */
var errorResolution = false;

function getSize(value, del) {
	var delimiter = 'x';
	if (del){
		delimiter = del;
	}
	var array = value.split(delimiter);
	return {w: array[0], h: array[1]};
}

function getSelectedElem(obj) {
	var select = byId(obj);
	for (var i = 0; i < select.options.length; i++) {
		if (select.options[i].selected) {
			return {text: select.options[i].text, value: parseInt(select.options[i].value)};
		}
	}
}

function setAreaObjects() {
	var areaX = byId('areaX');
	var areaY = byId('areaY');
	var areaWidth = byId('areaWidth');
	var areaHeight = byId('areaHeight');
	
	return {x: areaX, y: areaY, w: areaWidth, h: areaHeight};
}

function disabledOption(obj, index) {
	var select = byId(obj);
	var count = select.options.length;
	if ((index + 1) <= count) {
		index = index + 1;
	}
	for (var i = 0; i < index; i++) {
		select.options[i].disabled = false;
	}
	for (i = index; i < count; i++) {
		select.options[i].disabled = "disabled";
	}
}

function changeBorder(obj, err) {
	if (err) {
		obj.style.border = "1px solid #FF6600";
	} else {
		obj.style.border = "1px solid #AAAAAA";
	}
}

function checkInt(obj) {
	var re = /^\d+$/i;
	if (obj.value) {
		return re.exec(obj.value);
	}
	return true;
}

function ltrim(s) {
	var new_s;
	if (s.length >= 1) {
		new_s = s.replace(/^0+/, '');
		if (new_s) {
			return new_s;
		}
		return '0';
	}
	return '0'; 
}

function getInt(value) {
	return parseInt(ltrim(value));
}

function init() {
	var area = setAreaObjects();
	byId('err_mess').innerHTML = '&nbsp';
	errorResolution = false;
	changeBorder(area.x, false);
	changeBorder(area.y, false);
	changeBorder(area.w, false);
	changeBorder(area.h, false);
}

function setArea(objSel) {
	var area_elem;
	var area_size = [];
	
	var perm_elem = getSelectedElem('selectPermission');
	var perm_size = getSize(perm_elem.text);
	
	var area = setAreaObjects();
	
	if (objSel.selectedIndex != -1) {
		area_elem = objSel.options[objSel.selectedIndex];
		area_size = getSize(area_elem.text);
		area.w.value = area_size.w;
		area.h.value = area_size.h;
		area.x.value = (perm_size.w - area_size.w) / 2;
		area.y.value = (perm_size.h - area_size.h) / 2;
		
		init();
	}
}

function setResolution(objSel) {
	var perm_elem;
	var act_perm_value = '';
	var perm_size = [];	
	
	var area_list = byId('selectArea');
	var area_elem = getSelectedElem('selectArea');
	var act_area_value = area_elem.value;
	var area_size = getSize(area_elem.text);	
		
	var area = setAreaObjects();
	var selectedIndex = objSel.selectedIndex;
	
	if (selectedIndex != -1) {
		perm_elem = objSel.options[selectedIndex];
		act_perm_value = perm_elem.value;
		disabledOption(area_list, objSel.selectedIndex);
		perm_size = getSize(perm_elem.text);
		
		if (act_perm_value >= act_area_value) {
			area.x.value = (perm_size.w - area_size.w) / 2;
			area.y.value = (perm_size.h - area_size.h) / 2;
			area.w.value = area_size.w;
			area.h.value = area_size.h;			
		} else {
			area_list.selectedIndex = objSel.selectedIndex;
			area.w.value = perm_size.w;
			area.h.value = perm_size.h;
			area.x.value = 0;
			area.y.value = 0;
		}
		
		init();		
	}
}

function checkAllArea() {
	
	var area = setAreaObjects();
	var x = area.x;
	var y = area.y;
	var w = area.w;
	var h = area.h;
	
	if (x.value) {		
		if (!checkInt(x)) {
			byId('err_mess').innerHTML = "Значение должно содержать только цифры.";
			errorResolution = true;
			return;
		}	
		if (!checkAreaX(x)) {
			errorResolution = true;
			return;
		}
	} else {
		x.value = 0;
		errorResolution = false;
		return;
	}
	if (y.value) {
		if (!checkInt(y)) {
			byId('err_mess').innerHTML = "Значение должно содержать только цифры.";
			errorResolution = true;
			return;
		}
		if (!checkAreaY(y)) {
			errorResolution = true;
			return;
		}
	} else {
		y.value = 0;
		errorResolution = false;
		return;
	}
	if (w.value) {
		if (!checkInt(w)) {
			byId('err_mess').innerHTML = "Значение должно содержать только цифры.";
			errorResolution = true;
			return;
		}
		if (!checkAreaWidth(w)) {
			errorResolution = true;
			return;
		}
	} else {
		w.value = 320;
		errorResolution = false;
		return;
	}
	if (h.value) {
		if (!checkInt(h)) {
			byId('err_mess').innerHTML = "Значение должно содержать только цифры.";
			errorResolution = true;
			return;
		}
		if (!checkAreaHeight(h)) {
			errorResolution = true;
			return;
		}
	} else {
		h.value = 240;
		errorResolution = false;
		return;
	}
}

function checkAreaX(obj) {
	var value = 0;
	var areaWidth = byId('areaWidth');
	if (areaWidth.value) {
		if (getInt(areaWidth.value) > getSize(getSelectedElem('selectPermission').text).w) {
			byId('err_mess').innerHTML = "Введена слишком большая ширина для области захвата.+X";
			changeBorder(obj, false);
			changeBorder(areaWidth, true);
			return false;			
		}
		value = getInt(byId('areaWidth').value);
	}
	var s = getInt(obj.value) + value;
	if (s > getSize(getSelectedElem('selectPermission').text).w) {
		byId('err_mess').innerHTML = "Введено слишком большое смещение по координате \"x\".+X";
		changeBorder(obj, true);
		changeBorder(areaWidth, false);
		return false;
	}
	return true;	
}

function checkAreaY(obj) {
	var value = 0;
	var areaHeight = byId('areaHeight');
	if (byId('areaHeight').value) {
		if (getInt(areaHeight.value) > getSize(getSelectedElem('selectPermission').text).h) {
			byId('err_mess').innerHTML = "Введена слишком большая высота для области захвата.+Y";
			changeBorder(obj, false);
			changeBorder(areaHeight, true);
			return false;			
		}	
		value = getInt(areaHeight.value);
	}
	var s = getInt(obj.value) + value;
	if (s > getSize(getSelectedElem('selectPermission').text).h) {
		byId('err_mess').innerHTML = "Введено слишком большое смещение по координате \"y\".+Y";
		changeBorder(obj, true);
		changeBorder(areaHeight, false);
		return false;
	}
	return true;
}

function checkAreaWidth(obj) {
	if (getInt(obj.value) > getSize(getSelectedElem('selectPermission').text).w) {
		byId('err_mess').innerHTML = "Введена слишком большая ширина для области захвата.+WIDTH";
		changeBorder(obj, true);
		return false;	
	}
	var value = 0;
	var areaX = byId('areaX');
	if (areaX.value) {
		value = getInt(areaX.value);
	}
	if (getInt(obj.value) < 320) {
		obj.value = 320;
	}	
	var s = getInt(obj.value) + value;
	if (s > getSize(getSelectedElem('selectPermission').text).w) {
		byId('err_mess').innerHTML = "Введено слишком большое смещение по координате \"x\".+WIDTH";
		changeBorder(areaX, true);
		return false;			
	}
	return true;
}

function checkAreaHeight(obj) {
	if (getInt(obj.value) > getSize(getSelectedElem('selectPermission').text).h) {
		byId('err_mess').innerHTML = "Введена слишком большая высота для области захвата.+HEIGHT";
		changeBorder(obj, true);
		return false;	
	}
	var value = 0;
	var areaY = byId('areaY');
	if (areaY.value) {
		value = getInt(areaY.value);
	}
	if (getInt(obj.value) < 240) {
		obj.value = 240;
	}	
	var s = getInt(obj.value) + value;
	if (s > getSize(getSelectedElem('selectPermission').text).h) {
		byId('err_mess').innerHTML = "Введено слишком большое смещение по координате \"y\".+HEIGHT";
		changeBorder(areaY, true);
		return false;
	}
	return true;
}

function checkArea(obj) {
	if (!checkInt(obj)) {
		changeBorder(obj, true);
		errorResolution = true;
		return;
	}
	if (obj.id == 'areaX') {
		if (!checkAreaX(obj)) {
			errorResolution = true;
			return;
		}
	}
	if (obj.id == 'areaY') {
		if (!checkAreaY(obj)) {
			errorResolution = true;
			return;
		}
	}
	if (obj.id == 'areaWidth') {
		if (!checkAreaWidth(obj)) {
			errorResolution = true;
			return;
		}		
	}
	if (obj.id == 'areaHeight') {
		if (!checkAreaHeight(obj)) {
			errorResolution = true;
			return;
		}
	}
	changeBorder(obj, false);
	errorResolution = false;
	byId('err_mess').innerHTML = '&nbsp';
}

function getMaxResolution() {
	var perm_list = byId('selectPermission');
	var selectedIndex = perm_list.selectedIndex;
	var perm_elem;
	
	if (selectedIndex != -1) {
		perm_elem = perm_list.options[selectedIndex];
		perm_size = getSize(perm_elem.text);
		return {w: perm_size.w, h: perm_size.h}
	}
}

function getAllValueSize(objSel) {
	var select = byId(objSel);
	var selectedIndex = select.selectedIndex;
	var size = {};
	var w = new Array();
	var h = new Array();

	if (selectedIndex != -1) {
		for (var i = 0; i <= selectedIndex; i++) {
			size = getSize(select.options[i].text);
			w[i] = size.w;
			h[i] = size.h;
		}
	}
	
	return {w: w, h: h};
}

function assignIndex(w, h) {
	var all_size = getAllValueSize('selectPermission');
	var i = all_size.w.length-1;
	var index = i;

	while (i >= 0) {
		if ((w <= all_size.w[i]) && (h <= all_size.h[i])) {
			index = i;
		}
		i--;
	}

	byId('selectArea').selectedIndex = index;
}

function applyResolution() {
	if (!errorResolution) {
		var dx = 32;
		var dy = 16;
		var minResolutionWidth = 320;
		var minResolutionHeight = 240;
	
		var area = setAreaObjects();
		var x = area.x.value;
		var y = area.y.value;
		var w = area.w.value;
		var h = area.h.value;
	
		var maxResolution = getMaxResolution();
	
		x = Math.max(0, x);
		x = Math.min(maxResolution.w - minResolutionWidth, x);
	
		y = Math.max(0, y);
		y = Math.min(maxResolution.h - minResolutionHeight, y);
	
		x = Math.floor(x / dx) * dx;
		y = Math.floor(y / dy) * dy;
	
		w = Math.max(minResolutionWidth, w);
		w = Math.min(maxResolution.w - x, w);
	
		h = Math.max(minResolutionHeight, h);
		h = Math.min(maxResolution.h - y, h);

		assignIndex(w, h);
	
		w = Math.floor(w / dx) * dx;
		if (h != 600 && h != 240) {
			h = Math.floor(h / dy) * dy;
		}
		alert(x + '   ' + y + '   ' + w + '   ' + h + '   ' + maxResolution.w + '   ' + maxResolution.h);
	}
}

function checkValue(inp, defaultValue) {
	if (!inp.value) {
		inp.value = defaultValue;
		return;
	}
	changeBorder(inp, false);
	byId('err_mess').innerHTML = "&nbsp;";		
}

function msgErrorBlockPicture(id) {
	switch (id) {
		case "brightness": 
			return "Введено слишком большое значение для параметра \"Яркость\".";
			break;
		case "sharpness": 
			return "Введено слишком большое значение для параметра \"Резкость\".";
			break;
		case "saturation": 
			return "Введено слишком большое значение для параметра \"Насыщенность\".";
			break;
		case "contrast": 
			return "Введено слишком большое значение для параметра \"Контраст\".";
			break;
		case "qualityPicture": 
			return "Введено слишком большое значение для параметра \"Качество\".";
			break;
		case "shortExp": 
			return "Введённое значение для параметра \"Время экспозиции\" находится вне указанного диапазона.";
			break;			
		default: 
			return "Введено слишком большое значение.";
			break;
	}
}

function checkBlockPicture(id, defaultValue) {
	var inp = byId(id);
	var max_value = 255;
	if (!inp.value) {
		inp.value = defaultValue;
		return false;
	}	
	if (!checkInt(inp)) {
		changeBorder(inp, true);
		byId('err_mess').innerHTML = "Значение должно содержать только цифры.";
		return false;
	}
	if (id == 'sharpness') {
		max_value = 16;
	} 
	if (parseInt(inp.value) > max_value) {
		changeBorder(inp, true);
		byId('err_mess').innerHTML = msgErrorBlockPicture(id);
		return false;
	}
	changeBorder(obj, false);
	byId('err_mess').innerHTML = "&nbsp;";	
	return true;
}

function checkBlockLowLightMode(id, defaultValue) {
	var inp = byId(id);
	var max_value = 10;
	var min_value = 1;
	if (!inp.value) {
		inp.value = defaultValue;
		return false;
	}	
	if (!checkInt(inp)) {
		changeBorder(inp, true);
		byId('err_mess').innerHTML = "Значение должно содержать только цифры.";
		return false;
	}
	if ((parseInt(inp.value) > max_value) || (parseInt(inp.value) < min_value)) {
		changeBorder(inp, true);
		byId('err_mess').innerHTML = msgErrorBlockPicture(id);
		return false;
	}
	changeBorder(obj, false);
	byId('err_mess').innerHTML = "&nbsp;";	
	return true;	
}

function applayClick(id, defaultValue) {
	if (id == 'shortExp') {
		checkBlockLowLightMode(id, defaultValue);
	} else {
		checkBlockPicture(id, defaultValue);
	}
}


/* проверка выбора персоны */
function showError(elem, show, txt) {
	if (show) {
		changeBorder(elem, true);
		byId('err_mess').innerHTML = txt;
		//elem.focus();
	} else {
		changeBorder(elem, false);
		byId('err_mess').innerHTML = '&nbsp;';	
	}
}
function focusElem(inp, focus, defaultValue) {
	if (focus) {
		if ((inp.value == defaultValue) || (inp.value == '')) {
			inp.value = '';
			inp.style.color = '#505050';
		} 
	} else {
		if (inp.value == '') {
			inp.value = defaultValue;
			inp.style.color = '#868686';
		}
	}
	showError(inp, false);
}

function checkChoosePerson() {
	if (byId('pers_radio2').checked) {
		var name = byId('name_person');
		if ((name.value == '') || (name.value == 'Введите имя персоны') ) {
			showError(name, true, 'Введите имя персоны, пожалуйста.');
			return false;
		}
	} else if (byId('pers_radio1').checked) {
		var list = byId('persid');
		if (list.selectedIndex == 0) {
			showError(list, true, 'Выберите персону из базы, пожалуйста.');
			return false;
		}
	}
	return true;
}

function choosePerson(id) {
	byId(id).checked = true;
	var list = byId('persid');
	var name = byId('name_person');
	if (id == 'pers_radio1') {
		showError(name, false);
		if (list.selectedIndex > 0) {
			showError(list, false);	
		}
	} else if (id == 'pers_radio2') {
		showError(list, false);
	}
}

function initChoosePerson() {
	var list = byId('persid');
	var name = byId('name_person');
	showError(name, false);
	showError(list, false);
}

function showUploadBlock(show) {
	if (show) {
		byId('choose_person').style.display = 'none';
		byId('upload_files').style.display = 'block';
	} else {
		byId('upload_files').style.display = 'none';
		byId('choose_person').style.display = 'block';
	}
}

function showLearnCameraBlock(show) {
	if (show) {
		byId('choose_person').style.display = 'none';
		byId('learn_camera').style.display = 'block';
	} else {
		byId('learn_camera').style.display = 'none';
		byId('choose_person').style.display = 'block';
	}
}

function showFlash() {
	var check = checkChoosePerson();
	if (check) {
		showUploadBlock(true);
	}
}

function showLearnFlash() {
	var check = checkChoosePerson();
	if (check) {
		showLearnCameraBlock(true);	
	}
}

function chooseLang(elem) {
	var lang = elem.innerHTML;
	if (lang == 'RU') {
		elem.innerHTML = 'EN';
		elem.style.backgroundImage = "url('/files/images/lang_en2.gif')";
		elem.style.backgroundPosition = "0px 4px";
	} else {
		elem.innerHTML = 'RU';
		elem.style.backgroundImage = "url('/files/images/lang_ru.gif')";
		elem.style.backgroundPosition = "0px 5px";
	}
}

function positionScreen(idElement, obj) {
	var element = byId(idElement);

	var top = findPositionWithScrolling(element)[1] - obj.distY;
	if (getBodyScrollTop()) {
		top=top-getBodyScrollTop();
	} 
	var left = findPositionWithScrolling(element)[0] + element.offsetWidth + obj.distX;

	var sizeScreen = screenSize();

	var width = obj.w;
	var height = obj.h;

	if (left + width > sizeScreen.w) {
		left = findPositionWithScrolling(element)[0] - width - obj.distX;
	}

	if ((top + height) > sizeScreen.h) {
		top = sizeScreen.h - height - obj.distX;
	}

	return {top: top, left: left};	
}

function getBodyScrollTop()
{
	return self.pageYOffset || (document.documentElement && document.documentElement.scrollTop) || (document.body && document.body.scrollTop);
}

function findPositionWithScrolling( oElement ) {
  function getNextAncestor( oElement ) {
	var actualStyle;
	if( window.getComputedStyle ) {
	  actualStyle = getComputedStyle(oElement,null).position;
	} else if( oElement.currentStyle ) {
	  actualStyle = oElement.currentStyle.position;
	} else {
	  //fallback for browsers with low support - only reliable for inline styles
	  actualStyle = oElement.style.position;
	}
	if( actualStyle == 'absolute' || actualStyle == 'fixed' ) {
	  //the offsetParent of a fixed position element is null so it will stop
	  return oElement.offsetParent;
	}
	return oElement.parentNode;
  }
  if( typeof( oElement.offsetParent ) != 'undefined' ) {
	var originalElement = oElement;
	for( var posX = 0, posY = 0; oElement; oElement = oElement.offsetParent ) {
	  posX += oElement.offsetLeft;
	  posY += oElement.offsetTop;
	}
	if( !originalElement.parentNode || !originalElement.style || typeof( originalElement.scrollTop ) == 'undefined' ) {
	  //older browsers cannot check element scrolling
	  return [ posX, posY ];
	}
	oElement = getNextAncestor(originalElement);
	while( oElement && oElement != document.body && oElement != document.documentElement ) {
	  posX -= oElement.scrollLeft;
	  posY -= oElement.scrollTop;
	  oElement = getNextAncestor(oElement);
	}
	return [ posX, posY ];
  } else {
	return [ oElement.x, oElement.y ];
  }
}

function createInfoWindow(param) {
	var distX = 0;
	var distY = 0;
	if (param.distX) {
		distX = param.distX;
	}
	if (param.distY) {
		distY = param.distY;
	}
	var w1 = param.width;
	var h1 = param.height;

	var scr = screenSize();
	var win = byId(param.id);
	var fon = byId('block_fon');
	var content = byId(param.id+'_contWF');

	win.style.position = 'absolute';		
	win.style.left = positionScreen(param.elem, {w: w1, h: h1, distX: distX, distY: distY}).left +'px';
	var t = win.style.top = positionScreen(param.elem, {w: w1, h: h1, distX: distX, distY: distY}).top + getBodyScrollTop() +'px';
	
	var browserType = navigator.userAgent.toLowerCase();
	if (browserType.indexOf('msie') >= 0) {
		byId('block_fon').style.height = document.body.offsetHeight + 'px';
	}
	
	content.innerHTML = param.txt;
	content.parentNode.style.height = h1 - 62 + 'px';

	win.style.width = w1 + 'px';
	win.style.height = h1 + 'px';
	
	fon.style.display = 'block';
	win.style.display = 'block';	
}

function showHelp(btn, txt) {
	createInfoWindow({distX: 10, width: 400, height: 300, elem: btn, id: 'win_help', txt: txt})
}
function initButtonCamera(count) {
	var cl = '';
	for (var i = 1; i <= count; i++) {
		cl = byId("btn_play"+i).className;
		if (cl.indexOf("dis") == -1) {
			byId("btn_play"+i).className = 'btn_camera play';
		}	
	}
}

function addCamera() {
	//createInfoWindow({distX: 10, width: 400, height: 300, elem: btn, id: 'win_help', txt: txt})
	changeWindow({id: 'win_add', css: {width: '400px', height: '300px'}});
}

function getChooseCamera() {
	var radioObj = document.frm_learn.video;
	//alert(radioObj + '   ' + radioObj.length);
	alert(radioObj.length);
	if (radioObj.length) {
		alert('jjjjj');
		for (var i = 0; i < radioObj.length; i++) {
			if (radioObj[i].checked) {
				return radioObj[i].value;
			}
		}	
	} else {
		//alert('hhhhhhhhhhhhhh');
		alert(radioObj.checked);
	}
}

function chooseCamera(num) {
	byId('choose'+num).checked = 'checked';
}

function showIndicator(show) {
	var win = byId('indicator');
	var fon = byId('block_fon');
	if (show) {
		var w = 200;
		var h = 60;
		var scr = screenSize();
		win.style.top = (100 - h*100/scr.h)/3/100*scr.h + 'px';
		win.style.left = (scr.w - w) / 2 + 'px';	
		fon.style.display = 'block';
		win.style.display = 'block';
	} else {
		fon.style.display = 'none';
		win.style.display = 'none';
	}
}

function editNamePerson(num) {
	var id_name = 'nameperson'+num;
	var name = byId(id_name).innerHTML;
	byId('newname_person').value = name;
	byId('newname_id').value = num;
	//alert(name);
	changeWindow({id: 'win_editname', css: {width: '300px', height: '200px'}});
}

/****************************************** metro **************************************************/
/* поиск */
function search(inp, focus, txt) {
	var defaultValue = txt;
	if (focus) {
		if ((inp.value == defaultValue) || (inp.value == '')) {
			inp.value = '';
			inp.style.color = '#505050';
		} 
	} else {
		if (inp.value == '') {
			inp.value = defaultValue;
			inp.style.color = '#868686';
		}
	}
}

function showJournalPhoto(id) {
	var el = byId(id);
	var msg="<img src='/files/images/image_test3.jpg' alt='' style='width: 240px; height: 240px;' />";
	createInfoWindow({id: 'win_journalphoto', width: 250, height: 315, txt: msg, elem: el, distX: 5});
	//changeWindow({id: 'win_journalphoto', css: {width: '250px', height: '315px'}, txt: msg});
}
function check(inp, count) {
	if (inp.checked) {
		isCheckAll(count);
	} else {
		isChooseAll(false);		
	}
}
function isChooseAll(choose) {
	byId('choose_all').checked = choose;
	if (byId('choose_all2')) {
		byId('choose_all2').checked = choose;
	}	
}
function isCheckAll(count) {
	var count_checked = 0;
	for (var i = 1; i <= count; i++) {
		if (byId('check'+i).checked) {
			count_checked++;
		}
	}
	if (count == count_checked) {
		isChooseAll(true);	
	}	
}
function clickBalancer(id, inpId) {
	var el = byId(id);
	var inp = byId(inpId);
	el.style.display = (el.style.display == 'none') ? '' : 'none';
	inp.className = (inp.className == 'btn_balan_left') ? 'btn_balan_bottom': 'btn_balan_left';
}
/* специальные настройки */
function restartSystem(name_block) {
   var txt = createTextMessage({name_block: name_block});
   changeWindow({id: 'win_restart', css: {width: '300px', height: '200px'}, txt: txt});
}
function rebootComputer(name_block) {
   var txt = createTextMessage({name_block: name_block});
   changeWindow({id: 'win_reboot', css: {width: '300px', height: '200px'}, txt: txt});
}
function showUpdateWindow() {
	changeWindow({id: 'win_update', css: {width: '300px', height: '200px'}});
}
function showNameCamera(nameCamera) {
	byId("nameCamera").innerHTML = nameCamera;
}
/*function showCamera(btn, count) {
	var curr_class = btn.className;
	if (curr_class.indexOf('play') > -1) {
		initButtonCamera(count);
		btn.className = 'btn_camera stop_act';
	} else {
		btn.className = 'btn_camera play_act';
	}
}*/
function changeWhom(num){
	if (num==dperson){
		document.getElementById('swhom'+dperson).name='person';
		document.getElementById('swhom'+demployee).name='p';
		document.getElementById('whom'+dperson).style.display='block';
		document.getElementById('whom'+demployee).style.display='none';
	}else{
		document.getElementById('swhom'+demployee).name='person';
		document.getElementById('swhom'+dperson).name='p';
		document.getElementById('whom'+demployee).style.display='block';
		document.getElementById('whom'+dperson).style.display='none';
	}
}

function addSound() {
	changeWindow({id: 'win_sound', css: {width: '330px', height: '200px'}});
}
function checkFieldSound() {
	var name = byId('nameSound');
	var file = byId('fileSound');
	var cl;
	if (!name.value) {
		cl = name.className;
		if (cl.indexOf('error') < 0) {
			name.className = cl + ' error_border';
		}
		byId('error_block1').innerHTML = 'Напишите, пожалуйста, название звука.';
		byId('error_block1').style.display = 'block';
		return;
	}
	if (name.value) {
		byId('error_block1').style.display = 'none';
		cl = name.className;
		if (cl.indexOf('error') > -1) {
			name.className = cl.substr(0, cl.indexOf('error'));
		}		
	}	
	if (!file.value) {
		byId('error_block2').innerHTML = 'Выберите, пожалуйста, мелодию.';
		byId('error_block2').style.display = 'block';
		return;		
	}
	if (file.value) {
		byId('error_block2').style.display = 'none';
	}	
}
function checkSound(inp, num) {
	var txt;
	if (inp.checked) {
		txt = 'Звук успешно добавлен на событие "'+byId('event'+num).innerHTML+'".';
	} else {
		txt = 'Звук выключен.'
	}
	changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: txt});
}
function getExt() {
	var file = byId('fileSound').value;
	var array = file.split('.');
	if (array) {
		var ext = array[array.length-1];
		return ext;
	}
}

function testClick() {
	alert('testClick');
}
function disabledButton(id, change) {
	var btn = byId('btn_'+id);
	var clsName = btn.className;
	if (change) {
		if (clsName.indexOf('dis') > -1) {
			btn.disabled = false;
			btn.className = rtrim(clsName.substr(0, clsName.indexOf('dis')));
		}	
	} else {
		if (clsName.indexOf('dis') < 0) {
			btn.disabled = "disabled";
			btn.className = clsName + ' dis';
		}	
	}
}
function disabledButtonParam4(id1, id2, id3, id4) {
	var inp1 = byId(id1);
	var inp2 = byId(id2);
	var inp3 = byId(id3);
	var inp4 = byId(id4);
	var defaultValue1 = params[id1];
	var defaultValue2 = params[id2];
	var defaultValue3 = params[id3];
	var defaultValue4 = params[id4];
	var id_btn;	
	if (id1.indexOf('area') > -1) {
		id_btn = 'area';
	} else if (id1.indexOf('distr') > -1) {
		id_btn = 'distr';
	}
	if (inp1.value != defaultValue1) {
		disabledButton(id_btn, true);
	} else if ((inp2.value == defaultValue2) && (inp3.value == defaultValue3) && (inp4.value == defaultValue4)) {
		disabledButton(id_btn, false);
	} else {
		disabledButton(id_btn, true);
	}
}
function disabledButtonParam2(id1, id2) {
	var inp1 = byId(id1);
	var inp2 = byId(id2);
	var defaultValue1 = params[id1];
	var defaultValue2 = params[id2];
	var id_btn = 'time';	
	if (inp1.value != defaultValue1) {
		disabledButton(id_btn, true);
	} else if (inp2.value == defaultValue2) {
		disabledButton(id_btn, false);
	} else {
		disabledButton(id_btn, true);
	}
}
function checkField(id, defaultValue) {
	var inp = byId(id);
	var name = inp.id;
	
	if (name == 'areaX') {
		disabledButtonParam4('areaX', 'areaY', 'areaWidth', 'areaHeight');
	} else if (name == 'areaY') {
		disabledButtonParam4('areaY', 'areaX', 'areaWidth', 'areaHeight');	
	} else if (name == 'areaWidth') {
		disabledButtonParam4('areaWidth', 'areaX', 'areaY', 'areaHeight');	
	} else if (name == 'areaHeight') {
		disabledButtonParam4('areaHeight', 'areaX', 'areaY', 'areaWidth');
	} else if (name == 'distr1') {
		disabledButtonParam4('distr1', 'distr2', 'distr3', 'distr4');
	} else if (name == 'distr2') {
		disabledButtonParam4('distr2', 'distr1', 'distr3', 'distr4');
	} else if (name == 'distr3') {
		disabledButtonParam4('distr3', 'distr1', 'distr2', 'distr4');
	} else if (name == 'distr4') {
		disabledButtonParam4('distr4', 'distr1', 'distr2', 'distr3');
	} else if (name == 'interval') {
		disabledButtonParam2('interval', 'delay');
	} else if (name == 'delay') {
		disabledButtonParam2('delay', 'interval');
	} else if (inp.value != defaultValue) {
		disabledButton(name, true);
	} else {
		disabledButton(name, false);
	}
}
function checkChanges() {
	for (var i in params) {
		checkField(i, params[i]);		
	}
}
/* звуки и сигналы */
function saveProfile() {
	changeWindow({id: 'win_save_profile', css: {width: '300px', height: '200px'}});
}
function uploadProfile() {
	changeWindow({id: 'win_upload_profile', css: {width: '300px', height: '200px'}});
}
function defaultProfile() {
	var txt = 'Вернуться к настройкам по умолчанию?';
	changeWindow({id: 'win_default_profile', css: {width: '300px', height: '200px'}, txt: txt});
}
/* камера */
function getCountChilds(id, nameNode) {
	var parent = byId(id);
	var oChilds = parent.childNodes;
	var count = 0;
	for (var i = 0; i < oChilds.length; i++) {
		if (oChilds[i].nodeName == nameNode) {
			count++;
		}
	}
	return count;
}
function showBlockSettings(num) {
	var count = getCountChilds('list_settings', 'LI');
	var el;
	var inp;
	for (var i = 1; i <= count; i++) {
		el = byId('settings' + i);
		inp = byId('btn_arrow' + i);
		if (i == num) {
			el.style.display = (el.style.display == 'none') ? '' : 'none';
			inp.className = (inp.className == 'btn_set_left') ? 'btn_set_bottom': 'btn_set_left';		
		} else {
			el.style.display = 'none';
			inp.className = 'btn_set_left';
		}
	}
}
/* window indification */
function savePerson() {
	byId('divLearn').style.display='block'; 
	byId('bLearn').style.display='none';
}
/* visitor cards */
function checkVisitorCard() {
/*	var inp1 = byId("dateVisit1");
	var inp2 = byId("dateVisit2");
	var dateBeg = inp1.value;
	var dateEnd = inp2.value;
	var error = byId('err1');
	error.style.display = 'none';
	if ((!dateBeg) && (!dateEnd)) {
		error.innerHTML = 'Укажите период посещений.';
		error.style.display = 'block';
		inp1.style.borderColor = '#FF6600';
		inp2.style.borderColor = '#FF6600';
		return;
	}
	if (!dateBeg) {
		error.innerHTML = 'Укажите дату начала посещений.';
		error.style.display = 'block';
		inp1.style.borderColor = '#FF6600';		
		inp2.style.borderColor = '#AAAAAA';
		return;
	}
	if (!dateEnd) {
		error.innerHTML = 'Укажите дату окончания посещений.';
		error.style.display = 'block';
		inp1.style.borderColor = '#AAAAAA';
		inp2.style.borderColor = '#FF6600';
		return;	
	}
	var arr1 = dateBeg.split('.');
	var arr2 = dateEnd.split('.');
	if ((arr1[2] > arr2[2]) || (arr1[1] > arr2[1]) || (arr1[0] > arr2[0])) {
		error.innerHTML = 'Некорректно введена дата окончания посещений.';
		error.style.display = 'block';
		inp1.style.borderColor = '#AAAAAA';
		inp2.style.borderColor = '#FF6600';				
		return;
	}
	inp1.style.borderColor = '#AAAAAA';
	inp2.style.borderColor = '#AAAAAA';			
	error.style.display = 'none';
	
	var time = new Array();
	time['h1'] = byId('time11');
	time['h2'] = byId('time21');
	time['m1'] = byId('time12');
	time['m2'] = byId('time22');
	var h1 = time['h1'].options[time['h1'].selectedIndex].text;
	var h2 = time['h2'].options[time['h2'].selectedIndex].text;
	var m1 = time['m1'].options[time['m1'].selectedIndex].text;
	var m2 = time['m2'].options[time['m2'].selectedIndex].text;
	
	error = byId('err2');
	if ((h1 > h2) || ((h1 == h2) && (m1 >= m2))) {
		error.innerHTML = 'Некорректно введено время посещения.';
		error.style.display = 'block';
		time['h1'].style.borderColor = '#FF6600';
		time['h2'].style.borderColor = '#FF6600';
		time['m1'].style.borderColor = '#FF6600';
		time['m2'].style.borderColor = '#FF6600';
		return;
	}
	time['h1'].style.borderColor = '#AAAAAA';
	time['h2'].style.borderColor = '#AAAAAA';
	time['m1'].style.borderColor = '#AAAAAA';
	time['m2'].style.borderColor = '#AAAAAA';	
	error.style.display = 'none';
	*/
	return;
}
/* ident */
function getChooseCameraIdent() {
	var parent = byId('cameras');
	var oChilds = parent.childNodes;
	var nameNode = 'LI';
	var li;
	for (var i = 0; i < oChilds.length; i++) {
		if (oChilds[i].nodeName == nameNode) {
			li = oChilds[i];
			if (!li.className || (li.className == 'last')) {
				return li.id.split('_')[1];
			}
		}
	}
}
function showChooseCameraIdent() {
	var numcamera = getChooseCameraIdent();	
}


/*function showBlockSettings(num) {
	var count = getCountChilds('list_settings', 'LI');
	var el;
	var inp;
	for (var i = 1; i <= count; i++) {
		el = byId('settings' + i);
		inp = byId('btn_arrow' + i);
		if (i == num) {
			el.style.display = (el.style.display == 'none') ? '' : 'none';
			inp.className = (inp.className == 'btn_set_left') ? 'btn_set_bottom': 'btn_set_left';		
		} else {
			el.style.display = 'none';
			inp.className = 'btn_set_left';
		}
	}
}*/
function showListCameras(obj) {
	var obj = byId(obj);
	var inp = byId('btn_all');
	inp.className = (inp.className == 'btn_set_left') ? 'btn_set_bottom': 'btn_set_left';
	var text = (obj.innerHTML == 'Показать всё') ? 'Скрыть' : 'Показать всё';
	obj.innerHTML = text;
	var block = byId('all_cameras');
	block.style.display = (block.style.display == 'none') ? 'block' : 'none';	
}
/***************/
function createTitleWindow(param) {
	var distX = 0;
	var distY = 0;
	if (param.distX) {
		distX = param.distX;
	}
	if (param.distY) {
		distY = param.distY;
	}
	var w1 = param.width;
	var h1 = param.height;

	var scr = screenSize();
	var win = byId(param.id);
	if (win){
	var content = byId(param.id+'_contWF');

	win.style.position = 'absolute';		
	win.style.left = positionScreen(param.elem, {w: w1, h: h1, distX: distX, distY: distY}).left +'px';
	var t = win.style.top = positionScreen(param.elem, {w: w1, h: h1, distX: distX, distY: distY}).top + getBodyScrollTop() +'px';

	content.innerHTML = param.txt;

	win.style.width = w1 + 'px';
	if (h1) {win.style.height = h1 + 'px';}
	win.style.display = 'block';
	}
}
function closeTitle(id) {
	if (byId(id)) {
		byId(id).style.display = 'none';
	}
}