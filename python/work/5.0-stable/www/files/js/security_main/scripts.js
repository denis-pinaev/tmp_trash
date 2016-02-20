var prev_w = 0;
var prev_h = 0;
var prev_zoom_params = null;
var MIN_SIZE_SCREEN = {"width": 1280, "height": 720}; // минимальный размер экрана
function init() {
	initTooltip();
	var lo = readCookie('view_all_layout');
	if(lo){
		current_layout = parseInt(lo);
	}
	changeLayout(current_layout);
	changeDetectors();
	checkJournalForDetects();
	setInterval("checkSize()", 100);
}

function checkSize(){
	area = getFreeArea();
	if(prev_h!=area.height||prev_w!=area.width){
		changeLayout(current_layout);
	}
}
// увеличение камеры 
function zoomCameraCurrent(num) {
	if ((num==0 && (current_layout == 1 || current_layout == 3))||(current_layout == 2)){
		zoomAll(num);
	}else {
		zoomCamera(num, false);
	}
	return false;
}
// увеличение камеры для 1 и 3 просмотра
function zoomCamera(num, event) {
	var camera_big = getInfoCamera(0);
	var title_big = $("#camera_info_0").val();
	var event_big = $.trim($("#camera_0").attr("class").split("win_camera")["1"]);
	
	var camera_cur = getInfoCamera(num);
	var title_cur = $("#camera_info_" + num).val();
	var event_cur = $.trim($("#camera_" + num).attr("class").split("win_camera")["1"]);

	$("#camera_0").find("div.head_camera").html(camera_cur['text_name']);
	$("#camera_info_0").val(title_cur);
	$("#camera_id_0").val(camera_cur["camera_id"]);
	$("#camera_0").removeClass(event_big);
	if (event) $("#camera_0").addClass(event)
	else $("#camera_0").addClass(event_cur);
	
	$("#camera_" + num).find("div.head_camera").html(camera_big['text_name']);	
	$("#camera_info_" + num).val(title_big);
	$("#camera_id_" + num).val(camera_big["camera_id"]);
	$("#camera_" + num).removeClass(event_cur);
	$("#camera_" + num).addClass(event_big)
	
	var cur_elem = ALL_CAMERAS[0];
	ALL_CAMERAS[0] = ALL_CAMERAS[num];
	ALL_CAMERAS[num] = cur_elem;
	setCookie('uuid', ALL_CAMERAS[0]['uuid']);
	changeLayout(current_layout)
}
// удалить все классы для событий из заголовка для одной камеры
function initHeadCameraWindow(num) {
	$("#camera_" + num).removeClass("face person crowdDetect det_stream leftThings smokeDetect fireDetect flashDetect");
}
// удалить все классы / класс для событий из заголовка для всех камер
function initHeadCamerasWindow(event) {
	var cameras = $("#cameras div.win_camera");
	if (cameras.size() > 0) {
		$.each(cameras, function() {
			if (event) {
				$(this).removeClass(event);
			} else {
				$(this).removeClass("face person crowdDetect det_stream leftThings smokeDetect fireDetect flashDetect");
			}
		});
	}
}
// camera fullscreen
function zoomAll(num){
	var camera = $("#camera_" + num);
	if (prev_zoom_params) {
		prev_zoom_params = null;
		camera.css("z-index", 0);
		changeLayout(current_layout);
	}else {
		window.stop();
		camera.css("z-index", 99);
		var area = getFreeArea();
		w = area.width-4;
		h = area.height-2;
		var info = getInfoCamera(num);
		prev_zoom_params = { num: num, width: info.width, height: info.height, left: 0, top: 0, src:true };
		setLocationCamera({ num: num, width: w, height: h, left: 2, top: 0, src:true });
	}
}
// функция при наведении на камеру
function overCamera(obj) {
	if ((current_layout == 1) || (current_layout == 3)) {
		$(obj).css("cursor", "pointer");
	} else {
		$(obj).css("cursor", "default");
	}
}
// получить по id информацию о камере
function getInfoCamera(num) {
	return ALL_CAMERAS[num];
}
// получить свободную область
function getFreeArea(){
	var btnLog_width = 22;
	var size = screenSize();
	size.width = (size.width < MIN_SIZE_SCREEN["width"]) ? MIN_SIZE_SCREEN["width"] : size.width;
	size.height = (size.height < MIN_SIZE_SCREEN["height"]) ? MIN_SIZE_SCREEN["height"] : size.height;	
	var head_h = getHeightBlockHead();
	var filter_w = getWidthBlockFilter();	
	var width = size.width - filter_w;
	var height = size.height - head_h;
	if (isShowLog()) {
		width += filter_w - btnLog_width;
	}
	return { width: width, height: height }
}
// размер экрана
function screenSize() {
	return { width: $(window).width(), height: $(window).height() }
}
// получить высоту заголовка
function getHeightBlockHead() {
	var head = $("#header");
	var head_h = head.height() + parseFloat(head.css("padding-top")) + parseFloat(head.css("padding-bottom")) + parseFloat(head.css("margin-top")) + parseFloat(head.css("margin-bottom"));
	return head_h;
}
// получить ширину для блока Фильтр
function getWidthBlockFilter() {
	var filter = $("#filters_maps");
	var filter_w = filter.width() + parseFloat(filter.css("padding-left")) + parseFloat(filter.css("padding-right")) + parseFloat(filter.css("margin-left")) + parseFloat(filter.css("margin-right"));;
	return filter_w;
}
// установить расположение камеры
function setLocationCamera(param) {
	if(param.num>=ALL_CAMERAS.length) return;
	var camera = $("#camera_" + param.num);
	camera.css("width", param.width + "px");
	camera.css("height", param.height + "px");
	camera.css("left", param.left + "px");
	camera.css("top", param.top + "px");

	setMaxSizeForVideo(camera, param);
}
// установить максимальный размер для изображения
function setMaxSizeForVideo(camera, param) {
	var margin = 1; // расстояние от границ head_camera
	var head = camera.find("div.head_camera");
	var head_h = head.height() + 2*parseFloat(head.css("border-top-width"))
	var max_w = camera.width() - 2*margin;
	var max_h = camera.height() -  head_h - 2*margin;
	// для вертикального выравнивания
	var link = camera.find("div.video a");
	link.css("height", max_h + "px");
	link.css("line-height", max_h + "px");
	link.css("width", camera.width() - 2*margin + "px"); // чтобы изображение выравнивалось по горизонтали	
	// максимальные значения для изображения
	var img = camera.find("div.video a img");
	if (img.size() > 0) {
		img.css("max-width", max_w + "px");
		img.css("max-height", max_h + "px");
	}
	if (param.src) {
		var dx = 4;//32;
		var dy = 4;//16;
		param.width = Math.floor(param.width / dx) * dx;
		param.height = Math.floor(param.height / dy) * dy;
		//if (param.height != 600 && param.height != 240) {
		//	param.height = Math.floor(param.height / dy) * dy;
		//}		
		var info = getInfoCamera(param.num);
		{//if (info.width != param.width || info.height != param.height) {
			//img.attr("src", info.camera_url + "&width=" + param.width + "&height=" + param.height);
			info.width = param.width;
			info.height = param.height;
			if (info.timeout) clearTimeout(info.timeout);
			//info.timeout = setTimeout("changeURL("+param.num+","+max_w+", "+max_h+")", 100);
			changeURL(param.num,max_w, max_h);
		}
		
	}
}

function changeURL(num, max_w, max_h){
	var camera = $("#camera_" + num);
	var link = camera.find("div.video a");
	var img = camera.find("div.video a img");
	var info = getInfoCamera(num);
	if(num==0) window.stop();
	//alert("width=" + info.width + "&height=" + info.height);
	img.attr("src", info.camera_url + "&width=" + info.width + "&height=" + info.height);
	/*
    var title = img.attr("title");
	img.remove();
	//window.stop();
    var buffer = info.camera_url+"&width="+info.width+"&height="+info.height+'&random=' + (new Date()).getTime();
	link.append("<img alt='' src='" + buffer + "' title='"+ title +"' style='max-width: "+max_w+"; max-height: "+max_h+";'/>");
	/**/
}

//change layouts
function changeLayout(layout) {
	setActiveView(layout);
	current_layout = layout;
	setCookie('view_all_layout', layout);
	
	var area = getFreeArea();
	prev_w = area.width;
	prev_h = area.height;
	var carusel_height = prev_h - 85;
	$("#carousel").css("height", carusel_height + "px");
	var free_width = area.width;
	var free_height = area.height;
	var corr = (free_height/3)/(free_width/4);
	var cam_count = ALL_CAMERAS.length;
	var dx = 2;
	var dy = 2;
	if(cam_count<1) return;
	//window.stop();
	if(cam_count==1){
		setLocationCamera({ num: 0, width: free_width-dx, height: free_height-dy, left: dx, top: 0, src:true });
		return;
	}
	
	if (layout==2){
		var in_raw = Math.round(Math.sqrt(cam_count) / corr);
		if(cam_count == 4 && in_raw>2) in_raw = 2;
		var in_line = Math.ceil(cam_count/in_raw)
		var width = Math.floor(free_width/in_raw);
		var height = Math.floor(free_height/in_line);
		var x = 0;
		var y = 0;
		for(var i=0;i<cam_count;i++){
			setLocationCamera({ num: i, width: width-dx, height: height-dy, left: dx+x*(width), top: y*(height), src:true });
			x++;
			if(x>=in_raw){
				x = 0;
				y++;
			}
		}
		return;
	}
	if (layout==3){
		cam_count += 24;
		var in_raw = Math.max(5, Math.round(Math.sqrt(cam_count) / corr));
		if(cam_count - 25 < 6 && in_raw>6) in_raw = 6;
		var in_line = Math.max(5, Math.ceil(cam_count/in_raw));
		var width = Math.floor(free_width/in_raw);
		var height = Math.floor(free_height/in_line);
		var x = 0;
		var y = 0;
		var i = 0;
		setLocationCamera({ num: i, width: width*5-dx, height: height*5-dy, left: dx+x*(width), top: y*(height), src:true });
		var cam_num = 1;
		for(i=1;i<=cam_count;i++){
			if (x > 4 || y > 4) {
				setLocationCamera({ num: cam_num, width: width-dx, height: height-dy, left: dx+x*(width), top: y*(height), src:true });
				cam_num++;
			}
			x++;
			if(x>=in_raw){
				x = 0;
				y++;
			}
		}
		return;
	}
	if (layout==1){
		cam_count += 8;
		var in_raw = Math.max(3, Math.round(Math.sqrt(cam_count) / corr));
		if(cam_count - 9 < 4 && in_raw>4) in_raw = 4;
		var in_line = Math.max(3, Math.ceil(cam_count/in_raw));
		var width = Math.floor(free_width/in_raw);
		var height = Math.floor(free_height/in_line);
		var x = 0;
		var y = 0;
		var i = 0;
		setLocationCamera({ num: i, width: width*3-dx, height: height*3-dy, left: dx+x*(width), top: y*(height), src:true });
		var cam_num = 1;
		for(i=1;i<=cam_count;i++){
			if (x > 2 || y > 2) {
				setLocationCamera({ num: cam_num, width: width-dx, height: height-dy, left: dx+x*(width), top: y*(height), src:true });
				cam_num++;
			}
			x++;
			if(x>=in_raw){
				x = 0;
				y++;
			}
		}
		return;
	}
	
}
// выделить активный layout
function setActiveView(layout) {
	$("#list_views li a").removeClass("lv_act");
	$("#view" + layout).addClass("lv_act");
}
// создать всплывающее окно
function createTitleWindow(param) {
	var distX = 10;
	var distY = 10;
	var padding = 12;
	
	var win = $("#" + param.id); 	
	win.css("opacity", 0);
	win.show();
	if (param.txt) win.html(param.txt);	
	
	var left = param.event.pageX + distX;
	var top = param.event.pageY + distY;
	var width = win.width() + padding;
	var height = win.height() + padding;
	var scr = screenSize();
	if ( ( left + width ) > scr.width ) {
		left = scr.width - width;
	}
	if ( ( top + height ) > scr.height ) {
		top = scr.height - height - distY;
	}	
		
	var coord_left = left + "px";
	var coord_top = top + "px";
	win.css("left", coord_left);
	win.css("top", coord_top);
	win.css("opacity", 1);
}
// всплывающая подсказки для видео
function showInfoCamera(num, obj, event) {
	var info = $("#camera_info_" + num).val();
	createTitleWindow({id: "easyTooltip_camera", obj: $(obj), txt: info, event: event });
}
function hideInfoCamera() {
	$("#easyTooltip_camera").hide();
}
// отображать / не отображать журнал событий
function showLog(obj) {
	var block = $("#filters_maps");
	var btn = $(obj);
	
	var block_marginRight_min = "-342px"
	var block_marginRight_max = "0px"
	var btn_right_min = "0px"
	var btn_right_max = "322px"		
	var delay = 500;
	
	if (btn.attr("class").indexOf("show") < 0) {
		block.animate({
			marginRight: block_marginRight_min
			}, delay, function() {
			// Animation complete.
		});	
		//btn.addClass("show");
		btn.animate({
			right: btn_right_min
			}, delay, function() {
			btn.addClass("show");
		});			
	} else {
		btn.removeClass("show");
		block.animate({
			marginRight: block_marginRight_max
			}, delay, function() {
			// Animation complete.
		});		
		btn.animate({
			right: btn_right_max
			}, delay, function() {
			//btn.removeClass("show");
		});			
	}
}
// проверка скрыт или не скрыт журнал
function isShowLog() {
	var btn = $("#btn_log");
	return (btn.attr("class").indexOf("show") > -1);
}
// панель настроек
function panelSettings(obj) {
	var panel = $("#panel_settings");
	if (panel.css("display") == "none") {
		setCoordsPanel($(obj));
		panel.show();
	} else {
		panel.hide();
	}
}
// показать/скрыть панель настроек
function showPanelSettings(show) {
	var panel = $("#panel_settings");
	if (show) panel.show();
	else panel.hide();
}
// установить координаты для панели настроек
function setCoordsPanel(btn) {
	var panel = $("#panel_settings");
	var btn_coords = btn.offset();
	var left = btn_coords.left + btn.width() - panel.width() + "px";
	var top = btn_coords.top + btn.height() + "px";
	panel.css("left", left);
	panel.css("top", top);
}	
// вкл./выкл. увеличение камеры при срабатывании события
function checkZoomCameraEvent(obj) {
	if ($(obj).attr("checked")) IS_CAMERA_HAS_EVENT_ZOOM = true;
	else IS_CAMERA_HAS_EVENT_ZOOM = false;
}
// установить значение для настройки активной камеры
function setValueIsCameraHasEventZoom() {
	$("#is_zoom_camera_event").attr("checked", IS_CAMERA_HAS_EVENT_ZOOM);
}
// проверить событие на активность
function checkActiveEvent(event) {
	if (detectors_values.indexOf(event) > -1) {
		return event;
	}
	return "";
}