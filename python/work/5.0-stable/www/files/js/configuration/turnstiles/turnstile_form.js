function init() {
	initTooltip();
	checkLockCamerasBtns();	
}
// добавить камеры 
function addToCameras(state) {
	var count_checks = getCountCamerasListChecks("accesses");
	if (count_checks > 0) {
		var data = getDataCameras("accesses");
		addCamerasList(state);
		initListCameras(state);
		initListCameras("accesses");
		clearCamerasTemplates();
	}	
}
// получить кол-во выделенных камер
function getCountCamerasListChecks(state) {
	return $("#list_cameras_" + state + " li input[type=checkbox]:checked").size();
} 
// получить кол-во камер
function getCountCameras(state) {
	return $("#list_cameras_" + state + " li input[type=checkbox]").size();
}
// получить выделенные камеры
function getDataCameras(state) {
	var checks = $("#list_cameras_" + state + " li input[type=checkbox]:checked");
	var template = getBlockCamerasTemplates();
	var li;
	$.each(checks, function() {
		li = $(this).parent();
		var param = $("#cam_lablesource" + $(this).val()).val();
		var state = eval('(' + param + ')')['state'];
		var name_cam = eval('(' + param + ')').info;
		var attr = "";
		if (state == "off") {
			attr = " class='lc_noact short_descr' title='" + name_cam + " <strong>" + MESSAGES['camera_noact'] + "</strong>'";
		} else {
			attr = " class='short_descr' title='" + name_cam + "'";
		}
		template.append("<li" + attr + ">" + li.html() + "</li>");
		li.remove()
	});
	return template.html();	
}
// получить временный шаблон с камерами
function getBlockCamerasTemplates() {
	return $("#cameras_templates");
}
// очистить временный шаблон с камерами
function clearCamerasTemplates() {
	$("#cameras_templates").html("");
}
// инициализировать список камер
function initListCameras(state) {
	var count = getCountCameras(state);
	if (count > 0) {
		$("#list_cameras_" + state + " li:last").removeClass("lc_last");
		$("#list_cameras_" + state + " li.lc_odd").removeClass("lc_odd");
		$("#list_cameras_" + state + " li.lc_last").removeClass("lc_last");
		$("#list_cameras_" + state + " li:odd").addClass("lc_odd");
		$("#list_cameras_" + state + " li:last").addClass("lc_last");
		lockCamerasBtns(state, false);
	} else {
		lockCamerasBtns(state, true);
	}
	initTooltip();
}
// добавить данные в список камер
function addCamerasList(state) {
	var template = getBlockCamerasTemplates();
	$("#list_cameras_" + state).append(template.html());		
}
// блокировать/не блокировать кнопки
function lockCamerasBtns(state, lock) {
	if (lock) {
		$("div.in_out input[type=button]." + state).addClass("dis");
		$("div.in_out input[type=button]." + state).attr("disable", "disable");
	} else {
		$("div.in_out input[type=button]." + state).removeClass("dis");
		$("div.in_out input[type=button]." + state).attr("disable", false);
	}	
}
// проверка на блокировать/не блокировать кнопки
function checkLockCamerasBtns() {
	var count = getCountCameras("accesses");
	if (count == 0) lockCamerasBtns("accesses", true);
	count = getCountCameras("in");
	if (count == 0) lockCamerasBtns("in", true);
	count = getCountCameras("out");
	if (count == 0) lockCamerasBtns("out", true);	
}
// удаление камер
function deleteCameras(state) {
	var count_checks = getCountCamerasListChecks(state);
	if (count_checks > 0) {
		var data = getDataCameras(state);
		addCamerasList("accesses");
		initListCameras("accesses");
		initListCameras(state);
		clearCamerasTemplates();
	}
}
// сохранить настройки турникета 
function saveSettingsTurn() {
	var cameras_in = getIDCameras("in");
	$("#cameras_in").val(cameras_in)
	var cameras_out = getIDCameras("out");	
	$("#cameras_out").val(cameras_out)
}
// получить id камер
function getIDCameras(state) {
	var checks = $("#list_cameras_" + state + " li input[type=checkbox]");
	var ids = new Array();
	var i = 0;
	$.each(checks, function() {
		ids[i] = $(this).val();
		i++;
	});
	return ids;
}