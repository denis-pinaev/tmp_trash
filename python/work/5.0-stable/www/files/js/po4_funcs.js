function rtrim(s) {
	return s.replace(/\s+$/, '');
}
function ltrim2(s) {
	return s.replace(/^0+/, ''); 
}
function getSelectedElem(obj) {
	var select = byId(obj);
	for (var i = 0; i < select.options.length; i++) {
		if (select.options[i].selected) {
			return {text: select.options[i].text, value: select.options[i].value};
		}
	}
}
/* функции для окон */
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
/* сортировка */
function sort(inp) {
	var cur_class = inp.className;
	if (cur_class.indexOf('down') > -1) {
		inp.className = cur_class.substr(0, cur_class.indexOf('down')) + 'up';
	} else {
		inp.className = cur_class.substr(0, cur_class.indexOf('up')) + 'down';
	}
}
/* выбор языка */
function trimString(str, maxLen) {
	var str = rtrim(ltrim2(str));
	var len = str.length;
	if (len > maxLen){
		var nstr = str.substr(0, maxLen);
		var ostr = str.substr(maxLen, len);
		if (ostr.length > maxLen) {
			while (ostr.length > maxLen) {
				nstr = nstr + '<br />' + ostr.substr(0, maxLen);
				ostr =  ostr.substr(maxLen, len);
			}
		}
		nstr = nstr + '<br />' + ostr;
		return nstr;
	}
	return str;
}
/* выбор документов */
function chooseDoc(select) {
	var id = getSelectedElem(select).value;
	if (id == 1) {
		id = 'passport';
	} else {
		id = 'card';
	}
	if (id == 'passport') {
		byId('card').style.display = 'none';
	} else {
		byId('passport').style.display = 'none';	
	}	
	byId(id).style.display = 'block';
}
function clickBalancer(id, inpId) {
	var el = byId(id);
	var inp = byId(inpId);
	el.style.display = (el.style.display == 'none') ? '' : 'none';
	inp.className = (inp.className == 'btn_balan_left') ? 'btn_balan_bottom': 'btn_balan_left';
}
/* настройка звуков */
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
	byId('ext').value = getExt('fileSound');
	byId('frmAddSound').submit();
}