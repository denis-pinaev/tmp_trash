// инициализация
function init() {
	initTooltip();
	checkCountAndErrorsCameras();
}
// проверка на наличие камер и ошибок
function checkCountAndErrorsCameras() {
    var count = $("#count_cameras").val();
    var error = $("#error_cameras").val();
    var block = $("#block_show_camera");
	var block_data = $("#dataSettings");
	if (error != 'False') {
		block.hide();
		block_data.removeClass("block_info_cameras")
		return;
	}	
	if (count == 0) {
		block.hide();
		block_data.removeClass("block_info_cameras")
		return;
	} 	
	block_data.addClass("block_info_cameras")
    block.show()
}
// обновление списка камер
function refreshDataSettings() {
    if (settings_timeout) clearTimeout(settings_timeout);
	var only_active = $("#only_active_cameras").attr("checked") == "checked" ? 1 : 0;
    $.ajax({
        type: "GET",
        url: URLS["refresh_data"],
        data: {data: "True", only_active: only_active},
        success: function(msg){
			if (isProcessing <= 0) {
				setData(msg);
				initTooltip();
				checkPlayVideo();
				checkCountAndErrorsCameras();
			}
            settings_timeout = setTimeout('refreshDataSettings()', TIME_REFRESH);
        },
        error: function(msg) {
            settings_timeout = setTimeout('refreshDataSettings()', TIME_REFRESH);
        }
    });
}
// выделение всех строк
function selectedAllRow(inp) {
	var checks = $("#cameras td input[type=checkbox]");
	var checks_all = $("input[type=checkbox].check_all");
	if (inp.attr("checked")) {
		$.each(checks, function() {
			$(this).attr("checked", "checked");
		});
		checks_all.attr("checked", "checked");
	} else {
		$.each(checks, function() {
			$(this).attr("checked", false);
		});
		checks_all.attr("checked", false);	
	}
}
// выделение одной строки
function selectedRow(inp) {
	var checks_all = $("input[type=checkbox].check_all");
	var count = $("#cameras tr td input[type=checkbox]").size();
	var count_sel = 0;
	if (inp.attr("checked")) {
		count_sel = $("#cameras tr td input[type=checkbox]:checked").size();
		if (count_sel == count) {
			checks_all.attr("checked", "checked");
		}
	} else {	
		checks_all.attr("checked", false);
	}
}
// сохранить выделенные чекбоксы при обновлении списка
var check_buf = new Array();
function save_checks(){
	check_buf = new Array();
	var checks = $("#cameras tr td.td_first input[type=checkbox]:checked");
	var count = checks.size();
	if (count > 0) {
		var num = 0;
		$.each(checks, function() {
			num = $(this).attr("id").split("check")[1];
			check_buf.push(num);
		});
	}
}
// установить раннее выделенные чекбоксы при обновлении списка
function set_checks(){
	if (check_buf.length > 0) {
		var check;
		for (var i in check_buf) {
			check = $("#check" + check_buf[i]);
			if (check.size() > 0) check.attr("checked", "checked");
		}
		isCheckAll();
	}
}
// проверка при обновлении кнопок "Выделить всё"
function isCheckAll() {
	var count = $("#cameras tr td.td_first input[type=checkbox]").size();
	var count_checked = $("#cameras tr td.td_first input[type=checkbox]:checked").size();
	if (count == count_checked) {
		$("#dataSettings input[type=checkbox].check_all").attr("checked", "checked")
	}	
}
// обновить данные для списка камер
function setData(msg) {
	save_checks();
	$('#dataSettings').html(msg);
	set_checks();
	$("#cameras_count").html($("#count_cameras").val());
}
// создать всплывающее окно
function createTitleWindow(param) {
	var distX = param.distX ? param.distX : 0; 
	var distY = param.distY ? param.distY : 0; 
	var win = $("#" + param.id);   
	var pos_win = positionScreen({obj: param.obj, win_width: parseInt(win.css("max-width")), win_height: parseInt(win.css("max-height")), distX: distX, distY: distY});
	var coord_left = pos_win.left + "px";
	var coord_top = pos_win.top + "px";
	win.css("left", coord_left);
	win.css("top", coord_top);
	if (param.txt) win.html(param.txt);
	win.show();
}
// функционал для вкл./выкл. детекторов
function overDetector(obj) {
	var row = obj.parent().parent().parent();
	if (row.attr("class") != "tr_lock") {
		var det = getNameDetector(obj.find("a"));
		if (obj.attr("class") && (obj.attr("class").indexOf("det_noact") > -1)) {
			det = det + " <strong>" + DETECTORS["off"] + "</strong>"
		} else {
			det = det + " <strong>" + DETECTORS["on"] + "</strong>"
		}
		createTitleWindow({id: "easyTooltip_camera", obj: obj, width: 200, height: 200, distY: -25, distX: 5, txt: det });
	}
}
function outDetector() {
	$("#easyTooltip_camera").hide();
}
// получить название детектора
function getNameDetector(obj) {
	var det = obj.attr("class").split("_")[1];
	switch (det) {
		case "fire": return DETECTORS["fire"];
		case "smoke": return DETECTORS["smoke"];
		case "explosion": return DETECTORS["explosion"];
		case "things": return DETECTORS["things"];
		case "people": return DETECTORS["people"];
		case "stream": return DETECTORS["stream"];
		case "face": return DETECTORS["face"];
		case "person": return DETECTORS["person"];
	}
}
// показать/убрать крутишку при вкл./выкл. детектора
function showLoaderDetector(obj, show) {
	var block = obj.parent();
	var link = block.find("a");
	var loader = block.find("div.det_loader");
	if (show) {
		link.hide();
		link.after('<div class="det_loader"></div>');
	} else {
		if (loader.size() > 0) {
			loader.remove();
		}
		link.show();
	}
}
// текущее состояние детектора
function checkOnOffDetector(obj) {
	var block = obj.parent();
	if (block.attr("class") && (block.attr("class").indexOf("det_noact") > -1)) {
		return "off";
	} else {	
		return "on";
	}
}
// детекторы распознавания и идентификации
function turnModeScheduler(obj, uuid, mode, mode_need){
	isProcessing++;
	showLoaderDetector(obj, true);
	var state = checkOnOffDetector(obj);
	curr_obj = obj
	if (state == "off") {
		executeCommunicatorMethod('setModeScheduler', '{\'uuid\': \''+uuid+'\', \'mode\': \''+ mode_need +'\' }', 'IsTrue', '', '', '', 'turnDetectSuccessMode('+ mode + ','+ mode_need +')', 'turnDetectError()');
	} else {
		var mode_need2 = 0
		if (mode == 2) {//если текущие режим идентификации
			if (mode_need == 2) {//и ещё раз кликаем по идентификации
				mode_need2 = 1;//то требуется включить режим детектирования
			}
		}
		executeCommunicatorMethod('setModeScheduler', '{\'uuid\': \''+uuid+'\', \'mode\': \''+ mode_need2 +'\' }', 'IsTrue', '', '', '', 'turnDetectSuccessMode('+ mode + ','+ mode_need2 +')', 'turnDetectError()');
	}
}
// успешное вкл./выкл. детекторов распознавания и идентификации
function turnDetectSuccessMode(mode, mode_need) {
	var state = checkOnOffDetector(curr_obj);
	var block = curr_obj.parent();
	showLoaderDetector(curr_obj, false);
	if (state == "off") {
		block.removeClass('det_noact');
	} else {
		block.addClass('det_noact');
	}
	if (mode == 0) {
		if (mode_need == 2) {
			block.parent().find("li a.det_face").parent().removeClass('det_noact');
		} 		
	} else if (mode == 2) {
		if (mode_need == 0) {		
			block.parent().find("li a.det_person").parent().addClass('det_noact');
		} else if (mode_need == 2) {
			block.parent().find("li a.det_face").parent().removeClass('det_noact');
		}
	}	
	isProcessing--;
}
// детектор скопления людей
function turnCrowdDetect(obj, uuid){
	curr_obj = obj
	var state = checkOnOffDetector(curr_obj);
	isProcessing++;
	showLoaderDetector(curr_obj, true);
	if (state == "off") {
		executeMethodCrowdDetect(turnDetectSuccess, turnDetectError, 'setCameraParameter', uuid, 'true', '', '', '', 'crowdNeedAlert');
	} else {
		executeMethodCrowdDetect(turnDetectSuccess, turnDetectError, 'setCameraParameter', uuid, 'false', '', '', '', 'crowdNeedAlert');
	}		
}
// для вкл./выкл. детектора скопления людей
function executeMethodCrowdDetect(){
	var d = {name: arguments[2]};
	var successFunc = arguments[0];
	var errorFunc = arguments[1];
	for (var i=3; i < arguments.length; i++) {
		var z = i - 2;
		d['arg'+z] = arguments[i];
	}
	$.ajax({
		type: "POST",
		url: "/execute_method_balancer/",
		data: d,
		success: function(msg){
			if (msg == 'True') {
				successFunc();
			} else {
				errorFunc();
			}
		}, 
		error: function(msg) {
			errorFunc();
		}
	});
}
// остальные детекторы
function turnDetector(obj, uuid, com_host, com_port, nameDetect) { 
	isProcessing++;
	showLoaderDetector(obj, true);
	var state = checkOnOffDetector(obj);	
	curr_obj = obj;
	if (state == "off") {
		executeCommunicatorMethod('turnOnModeDetectScheduler', '{\'uuid\': \''+uuid+'\', \'detect\': \''+nameDetect+'\' }', 'IsTrue', '', '', '', 'turnDetectSuccess()', 'turnDetectError()');
	} else {
		executeCommunicatorMethod('turnOffModeDetectScheduler', '{\'uuid\': \''+uuid+'\', \'detect\': \''+nameDetect+'\' }', 'IsTrue', '', '', '', 'turnDetectSuccess()', 'turnDetectError()');
	}
}
// успешное вкл./выкл. детектора
function turnDetectSuccess() {
	obj = curr_obj
	var state = checkOnOffDetector(obj);
	var block = obj.parent();
	showLoaderDetector(obj, false);
	if (state == "off") {
		block.removeClass('det_noact');
	} else {
		block.addClass('det_noact');
	}
	isProcessing--;
}
// вкл./выкл. детектора с ошибкой
function turnDetectError() {
	showLoaderDetector(curr_obj, false);
	showMessage(ERRORS["on_off_detector"]);
	isProcessing--;
}
// видео с камеры
// получить состояние кнопка play
function getStateVideo(btn) {
	if (btn.attr("class").indexOf("play_act") > -1) {
		return "on";
	} else {
		return "off";
	}
}
// запустить/остановить видео
function playVideo(btn, uuid, com_host, com_port, com_mjpeg_port, camera_ip) {
	var state = getStateVideo(btn);
	var btns = $("#cameras tr td.td_play input[type=button]");
	if (state == "on") {
		btn.removeClass("play_act");
		video_play_id = 0;
	} else {
		btns.removeClass("play_act");
		btn.addClass("play_act");
		video_play_id = btn.attr("id");
		$("#host").html(com_host);
		$("#port").html(com_port);
		$("#mjpeg_port").html(com_mjpeg_port);
		$("#selected_camera_ip").html(camera_ip);
		$("#uuid").html(uuid);
		$("#video-frame-block").find("img").remove();
		window.stop();
		var buffer = 'http://'+com_host+':'+com_mjpeg_port+'/video?uuid='+uuid+'&width=640&height=480&fps={{ fps_of_the_cameras }}';
		$("#video-frame-block").append("<img alt='' src='" + buffer + "' width='400px' id='video-frame' />");		
	}
}
// видео для js-интерфейса
function playVideoJSVersion(btn, camera_name) {
	var state = getStateVideo(btn);
	if (state == "on") {
		$("#mini_camera_info").hide();
		$("#nameCamera").html(camera_name);
		$("#nameCamera").show();
		$("#video-frame-block").show();
	} else {
		$("#video-frame-block").hide();
		$("#mini_camera_info").show();
		$("#nameCamera").hide();
	}
}
// проверка для кнопки play
function checkPlayVideo() {
	if (video_play_id != 0) {
		$("#" + video_play_id).addClass("play_act");
	}
}
// добавление камеры
// настройки по умолчанию
var CAMERA = {
	MAC: '000000000000',
	PORT: '80'
}
// инициализация параметров для окна добавления камеры
function initParamsAddCamera() {
	$("#aip").val("");
	$("#amac").val(CAMERA.MAC);
	$("#aport").val(CAMERA.PORT);
	$("#ause_r").val("");
	$("#apas_s").val("");
	$("#anum").val("");
	$("#aurl").val("http://");
	$("#abitrate").val("");
	$("#afps").val("");
	$("#auid").val("");
}
// добавить камеру
function addCamera() {
	$("#communicators-select option:first").attr("selected", "selected");
	$("#types_cameras option:first").attr("selected", "selected");
	initParamsAddCamera();
	$("#bl_aip").show();
	$("#bl_abitrate").hide();
	$("#bl_afps").hide();
	$("#bl_aurl").hide();
	$("#bl_amac").show();
	$("#bl_aport").show();
	$("#bl_anum").hide();
	$("#bl_ause_r").show();
	$("#bl_apas_s").show();
	$("#bl_auid").hide();	
	changeWindow({id: 'win_add', css: {width: '400px', height: '300px'}});
}
// показывать поля в зависимости от типа камеры
function selectTypesCamera(select) {
	var type = $(select).find("option:selected").val();
	var win = $("#win_add");
	if (type == "AV2000") {
		// ip mac port user pass
		$("#bl_aip").show();
		$("#bl_abitrate").hide();
		$("#bl_afps").hide();
		$("#bl_aurl").hide();
		$("#bl_amac").show();
		$("#bl_aport").show();
		$("#bl_anum").hide();
		$("#bl_ause_r").show();
		$("#bl_apas_s").show();
		$("#bl_auid").hide();	
		win.css("height", "300px");
	}else if ((type == "AXIS") || (type == "BEWARD") || (type == "SONY") || (type == "MOBOTIX") || (type == "PANASONIC") || (type == "JVC")) {
		// AXIS // ip port user pass
		// BEWARD // ip port user pass
		// SONY // ip port user pass
		// MOBOTIX // ip port user pass
		// PANASONIC // ip port user pass
		// JVC // ip port user pass
		$("#bl_aip").show();
		$("#bl_abitrate").hide();
		$("#bl_afps").hide();
		$("#bl_aurl").hide();
		$("#bl_amac").hide();
		$("#bl_aport").show();
		$("#bl_anum").hide();
		$("#bl_ause_r").show();
		$("#bl_apas_s").show();
		$("#bl_auid").hide();
		win.css("height", "265px");
	} else if (type == "GOAL") {
		// GOAL // ip port num user pass
		$("#bl_aip").show();
		$("#bl_abitrate").hide();
		$("#bl_afps").hide();
		$("#bl_aurl").hide();
		$("#bl_amac").hide();
		$("#bl_aport").show();
		$("#bl_anum").show();
		$("#bl_ause_r").show();
		$("#bl_apas_s").show();
		$("#bl_auid").hide();
		win.css("height", "300px");
	} else if (type == "URL")  {
		// URL // url
		$("#bl_aip").hide();
		$("#bl_abitrate").hide();
		$("#bl_afps").hide();
		$("#bl_aurl").show();
		$("#bl_amac").hide();
		$("#bl_aport").hide();
		$("#bl_anum").hide();
		$("#bl_ause_r").hide();
		$("#bl_apas_s").hide();
		$("#aurl").val("http://");
		$("#bl_auid").hide();
		win.css("height", "235px");
	} else if (type == "DALLMEIER")  {
		// DALLMEIER // ip bitrate fps
		$("#bl_aip").show();
		$("#bl_abitrate").show();
		$("#bl_afps").show();
		$("#bl_aurl").hide();
		$("#bl_amac").hide();
		$("#bl_aport").hide();
		$("#bl_anum").hide();
		$("#bl_ause_r").hide();
		$("#bl_apas_s").hide();
		$("#bl_auid").hide();
		win.css("height", "235px");
/*	} else if (type == "TECHNOTEL")  {
		// TECHNOTEL // ip fps port uid
		$("#bl_aip").show();
		$("#bl_abitrate").hide();
		$("#bl_afps").show();
		$("#bl_aurl").hide();
		$("#bl_amac").hide();
		$("#bl_aport").show();
		$("#bl_anum").hide();
		$("#bl_ause_r").hide();
		$("#bl_apas_s").hide();
		$("#bl_auid").show();
		win.css("height", "270px");
*/
	} else {
		// OTHER camera // all parameters
		$("#bl_aip").show();
		$("#bl_abitrate").show();
		$("#bl_afps").show();
		$("#bl_aurl").show();
		$("#bl_amac").show();
		$("#bl_aport").show();
		$("#bl_anum").show();
		$("#bl_ause_r").show();
		$("#bl_apas_s").show();
		$("#bl_auid").hide();
		win.css("height", "440px");	
	}
	initParamsAddCamera();
}

// проверка наличия камеры перед добавлением 
function checkAddCamera() {
    if (checkSimilarCamera()){
        var host = $("#bl_aip");
        if (host.css('display') == "block"){                
    	    var txt = ERRORS["ip_camera_exist"]    	    
    	    txt = replace_string(txt, '{1}', $("#aip").val());
    	    txt = replace_string(txt, '{2}', $("#aport").val());
    	}else{    	                
    	    var txt = ERRORS["url_camera_exist"]
    	    txt = replace_string(txt, '{}', $("#aurl").val());
    	}   
		closeChangeWindow('win_add');
    	changeWindow({id: 'win_add_message', css: {width: '300px', height: '200px'}, txt: txt});       
        return false;
    }
	closeChangeWindow('win_add');
    addCameraOK();
}
// проверка наличия камеры в системе
function checkSimilarCamera(){
    var check = false;   
    var host = $("#bl_aip");
    if (host.css('display') == "block"){
        var data = {ip: $("#aip").val(), port: $("#aport").val()};
    }else{
        var data = {url: $("#aurl").val()};
    }
	$.ajax({
    	type: "POST",
    	async: false,
	   	url: URLS["check_similar_camera"],
	    data: data,
	    success: function(msg){
	        if (msg.status) check = true;
	    },
	    error: function(msg) {}
	});
	return check;
}
// добавление камеры
function addCameraOK() {
    closeChangeWindow('win_add_message');
    showIndicator(true);
    var url = $("#aurl").val();
    url = url.replace(/\&/g,'&amp;');
    executeCommunicatorMethod('addCamera', '{\'type\': "' + $("#types_cameras option:selected").attr("value") + '", \'ip\': "' + $("#aip").val() + '", \'mac\': "' + $("#amac").val() + '", \'port\': "' + $("#aport").val() + '", \'num\': "' + $("#anum").val() + '", \'user\': "' + $("#ause_r").val() + '", \'psw\': "' + $("#apas_s").val() + '", \'url\': "' + url + '"}', 'IsTrue', com_host[$("#communicators-select").attr("value")], com_port[$("#communicators-select").attr("value")], com_mjpeg_port[$("#communicators-select").attr("value")], 'addCameraOKFuncs("' + CAMERAS["add"] + '", true)', 'addCameraOKFuncs("' + ERRORS["add_camera"] + '")');
}
function addCameraOKFuncs(text, success) {
    showIndicator(false);
    showMessage(text);
    if ( success ) setTimeout('location.reload(true)', 2000);                               
}

// вкл./выкл. камеры
// всплывающая подсказка на кнопку Вкл./Выкл. камеру
function overTurnOnOffCamera(obj, camera) {
	var turn = obj.attr("class");
	if (turn.indexOf("on") < 0) {
		camera = camera + " <strong>" + CAMERAS["off"] + "</strong>";
	} else {
		camera = camera + " <strong>" + CAMERAS["on"] + "</strong>";	
	}
	createTitleWindow({id: "easyTooltip_camera", obj: obj, width: 200, height: 200, distY: -25, distX: 5, txt: camera });
}
function outTurnOnOffCamera() {
	$("#easyTooltip_camera").hide();
}
//включить/выключить камеру
function turnModePower(obj, uuid){
	isProcessing++;
	var state = checkOnOffPower(obj);
	curr_obj = obj;
	if (state == "off") {
		executeCommunicatorMethod('setModeScheduler', '{\'uuid\': \''+uuid+'\', \'mode\': \'0\' }', 'IsTrue', '', '', '', 'turnPowerSuccessMode()', 'turnPowerError()');
	} else {   
		executeCommunicatorMethod('setModeScheduler', '{\'uuid\': \''+uuid+'\', \'mode\': \'-1\' }', 'IsTrue', '', '', '', 'turnPowerSuccessMode()', 'turnPowerError()');
	}
}
// текущее состояние кнопки включения
function checkOnOffPower(obj) {
	if (obj.attr("class") && (obj.attr("class").indexOf("on") > -1)) {
		return "on";
	} else { 
		return "off";
	}
}
// успешное включение-отключение камеры
function turnPowerSuccessMode() {
	var state = checkOnOffPower(curr_obj);
	isProcessing--;
	if (state == "off") {  
		curr_obj.addClass('on'); 
		refreshDataSettings();
	} else {
		curr_obj.removeClass('on');
		var list = curr_obj.parent().parent().find("td.td_dets ul.list_detectors li");
		$.each(list, function() {
			$(this).addClass("det_noact");
			$(this).find("a").unbind("click");
		});
	}
}
// включение-отключение камеры с ошибкой
function turnPowerError() {
	isProcessing--;
}

// удаление камеры
var sendCamera = {}
// окно-подверждение для удаления
function cameraDelete(camera, uuid, id) {
	sendCamera = {uuid: uuid, camera: camera, id: id};
	var txt = replace_string(CAMERAS["delete"], '{}', camera);
	changeWindow({id: 'win_del', css: {width: '300px', height: '200px'}, txt: txt});
}
// удаление камеры
function okCameradelete() {
	showIndicator(true);
	$.ajax({
		type: "GET",
		url: URLS["delete_camera"],
		data: sendCamera,
		success: function(msg){
			showIndicator(false);
			if (msg == 'True') {
				refreshDataSettings();
			} else {
				var txt = replace_string(ERRORS["delete"], '{}', sendCamera.camera);
				showMessage(txt);
			}
		},
		error: function(msg) {
			showIndicator(false);
			var txt = replace_string(ERRORS["delete"], '{}', sendCamera.camera);
			showMessage(txt);
		}
	});	
}

// создание псевдонима для камеры
// окно для создания
function aliasCamera(name, val, cid) {
	$("#alias").html('<strong>' + name + '</strong>');
	$("#alias_cinp").val(val);
	$("#alias_cid").val(cid);
	changeWindow({id: 'win_alias', css: {width: '400px', height: '150px'}});
	setCaretTo("alias_cinp", val.length);
}
// установить курсор
function setCaretTo(obj, pos) {
	var obj = document.getElementById(obj); 
	if(obj.createTextRange) { 
		var range = obj.createTextRange(); 
		range.move("character", pos); 
		range.select(); 
	} else if(obj.selectionStart || obj.selectionStart == '0') { 
		obj.focus(); 
		obj.setSelectionRange(pos, pos); 
	}
}
// добавление псевдонима
function addAliasToCamera(){
	var cid = $("#alias_cid");
	var nm = $("#alias_cinp");
	if ((cid.size() > 0) && (nm.size() > 0)){
		$.ajax({
			type: "GET",
			url: "/set_alias_camera",
			data: {cid: cid.val(), name: nm.val()},
			success: function(msg){
				refreshDataSettings();
			},
			error: function(msg){
			}
		});
	}
}
// при клике на enter добавить псевдоним
function sendEnter(e) {
	if (e.keyCode == 13) {
		closeChangeWindow('win_alias');
		addAliasToCamera();
		return;
	}
	return;
}