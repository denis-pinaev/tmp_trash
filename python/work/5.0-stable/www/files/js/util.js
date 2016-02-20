//Определение активна вкладка или нет

// пример добавления функции
// windowOnFocusFunctions.push('checkForDetectorsAlerts()');
//
// пример прекращения какой либо деятельности при использовании ajax
//	if (!windowIsActive) {
//		return;
//	}

var windowIsActive = true;       // Переменная значение true значит вкладка активна
var windowOnFocusFunctions = []; // Массив вызываемых функций после возобновления активности вкладки
var windowOnBlurFunctions = [];  // Массив вызываемых функций для неактивной вкладки

$(window).focus(function() {
	if (!windowIsActive) {
		windowIsActive = true;
		for(var i = 0; i < windowOnFocusFunctions.length; i++ ) {
			eval(windowOnFocusFunctions[i]);
		}
	}
	
});
$(window).blur(function() {
	if (windowIsActive) {
		windowIsActive = false;
		for (var i = 0; i < windowOnBlurFunctions.length; i++) {
			eval(windowOnBlurFunctions[i]);
		}		
	}
});
// заменить подстроку
function replace_string(txt, cut_str, paste_str) { 
	var f = 0;
	var ht = '';
	ht = ht + txt;
	f = ht.indexOf(cut_str);
	if (f > -1) {
		ht = ht.substr(0,f) + paste_str + ht.substr(f + cut_str.length);
	}
	return ht.replace(cut_str, paste_str)
}
// прочитать куки
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
// установить куки
function setCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}
// проверка установлен ли флэш-плеер
function getFlashVersion(){
  // ie
  try {
	try {
	  // avoid fp6 minor version lookup issues
	  // see: http://blog.deconcept.com/2006/01/11/getvariable-setvariable-crash-internet-explorer-flash-6/
	  var axo = new ActiveXObject('ShockwaveFlash.ShockwaveFlash.6');
	  try { axo.AllowScriptAccess = 'always'; }
	  catch(e) { return '6,0,0'; }
	} catch(e) {}
	return new ActiveXObject('ShockwaveFlash.ShockwaveFlash').GetVariable('$version').replace(/\D+/g, ',').match(/^,?(.+),?$/)[1];
  // other browsers
  } catch(e) {
	try {
	  if(navigator.mimeTypes["application/x-shockwave-flash"].enabledPlugin){
		return (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]).description.replace(/\D+/g, ",").match(/^,?(.+),?$/)[1];
	  }
	} catch(e) {}
  }
  return '0,0,0';
}
function flashVersion() {
   var version = getFlashVersion().split(',').shift();
   if (version >= 10) { return true; } 
   else { return false; }
}
// выделение при наведении на строку таблицы
function overRow(tr) {
	$(tr).addClass("act");
}
function outRow(tr) {
	$(tr).removeClass("act");
}
// проверки на валидность
// проверить дату на корректность
function checkDateValidator(date) {
	var regexp = /^([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})$/;
	if (regexp.test(date)) {
		var arr = regexp.exec(date);
		if (arr[1] < 32 && arr[1] > 0 && arr[2] < 13 && arr[2] >= 0 && arr[3] > 1900) {		    
			var dt = new Date(arr[3], arr[2]-1, arr[1]);		    
			if (dt && dt.getDate()==arr[1] && (dt.getMonth()+1)==arr[2] && dt.getFullYear()==arr[3]) return true;
		}
		return false;
	} 
	return false;
}
// получить строку даты
function get_DateString(obj) {
    var br = $.browser;
	var browserType = navigator.userAgent.toLowerCase();
    if ((br.mozilla) || (br.safari && browserType.indexOf("chrome") < 0) || (br.opera)) {
        var str = obj['2'] + '/' + obj['1'] + '/' + obj['0'];
    } else {
        var str = obj['1'] + '-' + obj['0'] + '-' + obj['2'];
    }
    return str;
}
// проверка валидности периода дат
function checkDateRangeValidator(id_start, id_stop) {
	var objStart = $("#" + id_start).val().split(".");
	var objStop = $("#" + id_stop).val().split(".");
	var strStart = get_DateString(objStart);
	var strStop = get_DateString(objStop);
	var intStart = Date.parse(strStart);
	var intStop = Date.parse(strStop);
	return [intStart, intStop];
}
// всплывающие подсказки
function initTooltip() {
    $(".short_descr").easyTooltip();        
}