var COUNT_WINDOWS_DETECTORS = 80;
$(function() {
	init();
});
// инициализация
function init() {
	initTooltip();
	initFuncs();
}
//инициализация всплыв подсказок
function initTooltip(){
	$("#carousel_ident li .param_photo").easyTooltip();
	$("#carousel_ident li .block_photo_cam").easyTooltip();
	$("#carousel_faces li .param_photo").easyTooltip();
	$(".short_descr").easyTooltip();
}
// инициализация функций
function initFuncs() {
	$("a.link_action_head").click(function() {
		showBlockAction($(this));
		return false;
	});
	$("#link_show_all_ident").click(function() {
		createIdentsWindow();
		changeWindow2({
			id: "win_ident",
			css: {width: 785, height: 435}
		});	
		return false;
	});
	$("#link_show_all_faces").click(function() {
		createDetectsWindow();
		changeWindow2({
			id: "win_faces",
			css: {width: 810, height: 450}
		});		
		return false;
	});
	$("#link_show_all_things").click(function() {
		createObjectsWindow();
		changeWindow2({
			id: "win_things",
			css: {width: 730, height: 430}
		});		
		return false;
	});
}
// сделать камеру активной
function activeCamera(obj_link) {
	var block = obj_link.parent();
	if (block.attr("class").indexOf("noact") < 0) {
		initListCameras();
		block.addClass("act");
	}
}
// 
function showInfoBigCamera(obj_link) {
	var info = $("#info_bigcamera");
	if (info.css("display") == "none") {
		getBigCameraInfo();
		info.slideDown("fast");
	} else {
		info.slideUp("fast");
	}
}
function initListCameras() {
	$("#cameras div.camera").removeClass("act");
}
// скрыть / показать блоки действий
function showBlockAction(link) {
	var block = link.parent().next();
	if (block.css("display") == "block") {
		block.slideUp("normal", function() {
			link.addClass('lah_turn');
		});
	} else {
		block.slideDown("normal", function() {
			link.removeClass('lah_turn');
		});
	}
}
// window warning
function initFuncsWindowWarning() {
	$("#window_message_warning .window_message_warning_close a").click(function() {
		windowWarning(false);
		return false;
	});
}
function windowWarning(show, param) {
	var win = $("#window_message_warning");
	if (show) {
		var width = parseInt(win.css("width"));
		var left = ($(window).width() - width)/2 + "px";
		win.css("left", left);
		win.find("div.window_message_warning_img").html('<img alt="" src="' + param.img + '" />');
		win.find("div.window_message_warning_info").html(param.info);
		win.removeClass("danger");
		if (param.danger) {
			win.addClass("danger");
		}
		win.slideDown("normal");
	} else {
		win.slideUp("normal");
	}
}
// удалить окно
function deleteWindowDetector(id) {
	$("#" + id).remove();
}
// удалить все окна
function deleteAllWindowDetector() {
	var wins = $("div.winDetector");
	$.each(wins, function() {
		if ($(this).css("display") == "block") {
			$(this).remove();
		}
	});
	$("#easyTooltip").remove();
}
function truncChar(value, arg) {
	if (value.length > arg) {
		value = value.substring(0, arg) + "...";
	}
	return value;
}
function createWindowDetector(d_color, d_string, d_time, d_image, d_camera_full_name, ident) {
	var wins = $(".winDetector");
	var count = 0;
	$.each(wins, function() {
		if ($(this).css("display") == "block") {
			count++;
		} 
	});
	if (count >= COUNT_WINDOWS_DETECTORS) {
		window.location.reload();
	} else {
		var win = $('<div id="win_detector_' + count + '" style="display: none;" class="winFloating winDetector"></div>');
		$("body").append(win);
		win.html($("#win_detector").html());
		var css = {width: 420, height: 405};
		var count_msg = "";
		if (count > 0) { 
			count_msg = NOT_SEEN + ": <strong>" + count + "</strong>";
		}
		win.find("div.bodyWF div.count").html(count_msg);		
		win.find("div.headWF_txt").css("color", d_color);
		win.find("div.headWF_txt").html(d_string);
		win.find(".koeff_time").html(d_time);
		win.find(".preview_camera_ip").html(truncChar(d_camera_full_name, 48));
		win.find(".preview_camera_ip").attr("title", d_camera_full_name);
		if (ident) {
		    win.find("div.winDetector_img").hide();
		    win.find("div.winDetector_ident").show();		    
		    if (ident.base_image) {
		        win.find("img.preview_base_ident").attr("src","data:image/gif;base64," + ident.base_image);
		    }
		    if (d_image) {
		        win.find("img.preview_camera_ident").attr("src","data:image/gif;base64," + d_image);
		    }
		    win.find("span.photo_coeff").html("C<sub>sm</sub>="+ident.coeff);
		    var fio_title = ident.fio;
		    if (isOperator) {
		        win.find("div.fio").html(fio_title);
		    } else {
		        win.find("div.fio a").html(fio_title);
		    }
		    win.find("div.fio").attr("title", ident.fio);
		    if (urls_arr[ident.group_pk]) {
		        url = urls_arr[ident.group_pk] +""+ ident.id + "/?group=" + ident.group_pk;
		        if (isOperator) {
		            win.find("div.photo_ident_from_camera").html(win.find("div.photo_ident_from_camera a").html());
		            win.find("div.photo_ident_from_base").html(win.find("div.photo_ident_from_base a").html());
		        } else {
		            win.find("div.fio a").attr("href", url);
		            win.find("div.photo_ident_from_camera a").attr("href", url);
		            win.find("div.photo_ident_from_base a").attr("href", url);
		        }
		    }
		} else {
		    win.find("div.winDetector_ident").hide();
		    win.find("div.winDetector_img").show();
		    win.find("img.preview_image").attr("src","data:image/gif;base64," + d_image);
		}
		changeWindow2({
			id: win.attr("id"),
			css: css,
			noblock: true,
			close: 'deleteWindowDetector(\'' + win.attr("id") + '\')'
		});		
		$(".short_descr").easyTooltip();		
	}
}

function createArrowIdent(params) {
	var height = 16;
	var width = 17;
	var distY = 7;
	var distX = 4;
	var widthFace = 45;
	if (params.width > widthFace) {
		var coeff = params.width/widthFace;
		height = height*coeff;
		width = width*coeff;
		distY = distY*coeff;
		distX = distX*coeff;	
	}
	var coords = [[parseInt(width/2), height], [0, distY], [distX, distY], [distX, 0], [width - distX, 0], [width - distX, distY], [width, distY]];
	distX = (params.x + parseInt(params.width/2)) - parseInt(width/2);
	distY = params.y - parseInt(height);	
	for (var i = 0; i < coords.length; i++) {
		coords[i][0] = coords[i][0] + distX;
		coords[i][1] = coords[i][1] + distY;
	}
	svgObjects.polygon(coords, {fill: params.color, stroke: params.color, strokeWidth: 1, fillOpacity: 0.4, class_: "svgObjects_arrow"});
}