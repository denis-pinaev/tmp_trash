function buttonStatus(btn, status) {
	var w = btn.offsetWidth;
	var h = btn.offsetHeight;
	var path = 'images/button'+w+'x'+h+'_'+status+'.gif';
	btn.style.backgroundImage = "url("+path+")";
}
function linkStatus(link, status) {
	var path = 'images/button90x24_'+status+'.gif';
	link.style.backgroundImage = "url("+path+")";
}

function byId(node) {
	return typeof node == 'string' ? document.getElementById(node) : node;
}

function checkAll(inp, count) {
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

function checkPhoto(inp, count) {
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
		if (byId('check'+i).checked) {
			count_checked++;
		}
	}
	if (count == count_checked) {
		document.getElementById('choose_all').checked = true;
		if (document.getElementById('choose_all2')) {
			document.getElementById('choose_all2').checked = true;
		}	
	}	
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

function createTextMessage(param) {
	switch (param.name_block) {
		case "persons": 
			return "Выберите, пожалуйста, хотя бы одну персону.";
			break;
		case "persons_del":
			return "Вы, действительно, хотите удалить выбранных персон("+param.count+")?";
			break;
		case "persons_zeroing": 
			return "Вы, действительно, хотите удалить базу персон?";
			break;
		case "lists_zeroing": 
			return "Выберети для удаления только пустые списки.";
			break;
		default: 
			return "Выберите, пожалуйста, хотя бы одно изображение.";
			break;
	}
}

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

function showMessage(txt) {
	changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: txt});
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

	var t = win.style.top = (scr.h) / 2 - parseInt(win.style.height) + 'px';
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
		elem.style.backgroundImage = "url('images/lang_en2.gif')";
		elem.style.backgroundPosition = "0px 4px";
	} else {
		elem.innerHTML = 'RU';
		elem.style.backgroundImage = "url('images/lang_ru.gif')";
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
function showCamera(btn, count) {
	var curr_class = btn.className;
	if (curr_class.indexOf('play') > -1) {
		initButtonCamera(count);
		btn.className = 'btn_camera stop_act';
	} else {
		btn.className = 'btn_camera play_act';
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

function executeCMD() {
	$.ajax({
		type: "POST",
		url: "/wizard/restart-cs/",
		data: {},
		success: function(msg){
			location.href='/settings/';
		},
		error: function(msg) {
			location.href='/settings/';
		}
	});
	//$.post('', {
	//	}, function(data) {
	//	}, "json");
}
