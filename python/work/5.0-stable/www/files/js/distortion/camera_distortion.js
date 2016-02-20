var blockButtons = false;
// инициализация
function init() {
	initTooltip();
	initTooltipGrid();
	initFuncsCurrent();
	initFuncsDraw();
	checkModelDistortion();
	checkBrowserType();
}
function initTooltip() {
	$(".short_descr").easyTooltip();
}
function initTooltipGrid() {
    $("#btn_grid").easyTooltip({
        useElement: "tooltip_grid"
    });  
}
// инициализация общих функций
function initFuncsCurrent() {
	$("input[name=model]").click(function() {
		checkModelDistortion();
	});
	$("#btn_calculate").click(function() {
		sendCalculatedDistortion();
	});
	$("#btn_show").click(function() {
		if(!blockButtons){
			getImageWithDistortion();
		}
	});
	$("ul.menu_camera li input[type=button]").mouseover(function() {
		menuCameraElementState($(this), 'over');
	});
	$("ul.menu_camera li input[type=button]").mouseout(function() {
		menuCameraElementState($(this), 'out');
	});
	$("ul.menu_camera li input[type=button]").mousedown(function() {
		menuCameraElementState($(this), 'down');
	});
	$("ul.menu_camera li input[type=button]").mouseup(function() {
		menuCameraElementState($(this), 'up');
	});		
	$("ul.menu_camera li .block_upload2").mouseover(function() {
		menuCameraElementState($(this), 'over');
	});
	$("ul.menu_camera li .block_upload2").mouseout(function() {
		menuCameraElementState($(this), 'out');
	});
	$("ul.menu_camera li .block_upload2").mousedown(function() {
		menuCameraElementState($(this), 'down');
	});
	$("ul.menu_camera li .block_upload2").mouseup(function() {
		menuCameraElementState($(this), 'up');
	});	
}
// проверка типа браузера на chrome, в зависимости от этого изменён выбор файла при нажатии на иконку загрузки.
function checkBrowserType() {
	var browserType = navigator.userAgent.toLowerCase();
	if (browserType.indexOf("chrome") > 0) {
		$("#image_file2").hide();
		$("ul.menu_camera li .block_upload2").mousedown(function() {
			menuCameraElementState($(this), 'down');
			$("#image_file2").click();
		});		
	}
}
function rtrim(s) {
	return s.replace(/\s+$/, '');
}
function menuCameraElementState(obj, state) {
	var block = obj.parent();
	if (block.attr("class") && (block.attr("class").indexOf("not_avail") > -1)) {
	} else {
		if (obj.attr("class").indexOf("block_upload2") > -1) {
			var cl = rtrim(obj.attr("class").split(" ")[2]);
		} else {
			if (obj.attr("class").indexOf("grid") < 0) {
				var cl = rtrim(obj.attr("class").split("short_descr")[0]);
			} else {
				var cl = "grid";
			}
		}
		if ((state == "over") || (state == "down")) {
			obj.addClass(cl + "_" + state);
			return;
		}
		if (state == "out") {
			obj.removeClass(cl + "_over");
			return;
		}
		if (state == "up") {
			obj.removeClass(cl + "_down");
			return;
		}
	}
}
// проверка какая дисторсия выбрана
function checkModelDistortion() {	
	var inp = $("input[name=model]:checked");
	var block_intensity = $("#block_intensity");
	if (inp.attr("id") == "model3degree") {
		block_intensity.find("input[type=text]").attr("disabled", "disabled");
		block_intensity.find("input[type=button]").attr("disabled", "disabled");
		block_intensity.addClass("bl_param_dis");
	} else {
		block_intensity.find("input[type=text]").attr("disabled", false);
		block_intensity.find("input[type=button]").attr("disabled", false);
		block_intensity.removeClass("bl_param_dis");
	}
}
// посчитать дисторсию
function calculateDistortion() {
	if (points.length > 0) {
		alert("Завершите создание ломаной");
		return;
	}
	if (pointsResult.length > 0) {
		var point = {};
		var point1 = {};
		var point2 = {};
		for (var i in pointsResult.items) {
			alert("Ломаная " + i);
			point = pointsResult.getItem(i);
			for (i in point) {
				point1 = point[i];
				j = parseInt(i) + 1;
				point2 = point[j];
				if (typeof(point2) != "undefined") {
					alert(point1.x + " " + point1.y + " ; " + point2.x + " " + point2.y);
				}
			}
		}
	}
}
// функция, которая нужна для того, чтобы сформировать hash-массив
function Hash() {
	this.length = 0;
	this.m = 0;
	this.items = new Array();
	for (var i = 0; i < arguments.length; i += 2) {
		if (typeof(arguments[i + 1]) != 'undefined') {
			this.items[arguments[i]] = arguments[i + 1];
			this.length++;
		}
	}
	this.removeItem = function(in_key) {
		var tmp_previous;
		if (typeof(this.items[in_key]) != 'undefined') {
			this.length--;
			var tmp_previous = this.items[in_key];
			delete this.items[in_key];
		}
		return tmp_previous;
	}
	this.getItem = function(in_key) {
		return this.items[in_key];
	}
	this.setItem = function(in_key, in_value) {
		var tmp_previous;
		if (typeof(in_value) != 'undefined') {
			if (typeof(this.items[in_key]) == 'undefined') {
				this.length++;
				this.m++;
			} else {
				tmp_previous = this.items[in_key];
			}
			this.items[in_key] = in_value;
		}
		return tmp_previous;
	}
	this.hasItem = function(in_key)	{
		return typeof(this.items[in_key]) != 'undefined';
	}
	this.clear = function()	{
		for (var i in this.items) {
			delete this.items[i];
		}
		this.length = 0;
	}
}
var svgDraw;                   // svg, содержит линии, которые рисуют в данный момент
var points = new Hash();       // текущий массив из точек
var pointsResult = new Hash(); // массив-результат из точек
var params = new Array();      // массив в котором содержаться первоначальные значения параметров дисторсии

var STROKE_COLOR = "#ff0000";  // цвет линии
var STROKE_WIDTH = 2;          // ширина линии
var FILL = "#ffffff";          // цвет заливки
var FILL_OPACITY = 0;          // прозрачность заливки
var show_grid = false;

// инициализация объекта svg для линий
function initSvgDraw(svg) {
	svgDraw = svg;
}
function initFuncsDraw() {
	$("#svgdraw").svg({onLoad: initSvgDraw});
	$("#btn_polygon").click(function() {
		if(!blockButtons){
			if ($(this).attr("class").indexOf("_act") < 0) {
				$(this).addClass("polygon_act");
				addDraw();
			} else {
				$(this).removeClass("polygon_act");
				deleteDraw();
			}
		}
	});
	$("#btn_clear").click(function() {
		if(!blockButtons){
			deleteAllLines();
		}
	});
	
	$("#btn_grid").click(function() {
		var block = $("#tooltip_grid");
		if(!blockButtons){
			if ($(this).attr("class").indexOf("_act") < 0) {
				$(this).addClass("grid_act");
				show_grid = true;
				block.html(TOOLTIP_GRID["hide"]);
			} else {
				$(this).removeClass("grid_act");
				show_grid = false;
				block.html(TOOLTIP_GRID["show"]);
			}
		}
		initTooltipGrid();
	});
}
// удалить все линии
function deleteAllLines() {
	$("#btn_polygon").removeClass("polygon_act");
	deleteDraw();
	deleteResult();
}
// удалить линии результата
function deleteResult() {
	pointsResult.clear();
}
// добавить рисование
function addDraw() {
	var block_draw = $('#svgdraw');
	block_draw.bind("click", function(eventObj) {
		drawZoneTypePolygon(eventObj);
		hideMenu();
	});	
}
// рисование ломаной с помощью линий
function drawZoneTypePolygon(eventObj) {
	var location = $('#svgdraw').offset();
	var x = parseInt(eventObj.pageX - location.left);
	var y = parseInt(eventObj.pageY - location.top);
	var count = points.m;
	points.setItem(count, { x: x, y: y });
	drawRect({ x: x, y: y, number: count });
}

var GRID_LINE_WIDTH = 1;
var GRID_LINE_COLOR = '#00ff00';
var GRID_BLOCK_SIZE = 30;

// рисование линий
function drawLines() {
	svgDraw.clear();
	
	//grid rendering
	if(show_grid){
		var d = 0;
		for (var y = 0; y < frame_height; y++){
			if(d == GRID_BLOCK_SIZE){
				svgDraw.line(0, y, frame_width, y, {stroke: GRID_LINE_COLOR, strokeWidth: GRID_LINE_WIDTH});
				d = 0;
			}
			d++;
		}
		
		d = 0;
		for (var x = 0; x < frame_width; x++){
			if(d == GRID_BLOCK_SIZE){
				svgDraw.line(x, 0, x, frame_height, {stroke: GRID_LINE_COLOR, strokeWidth: GRID_LINE_WIDTH});
				d = 0;
			}
			d++;
		}
	}
	
	var point1 = [];
	var point2 = [];
	var j = 0;
	var count = points.length;
	if (count > 1) {
	    point1 = false;
         for (var i in points.items) {
			point2 = points.getItem(i);
			if (point1 && typeof(point2) != "undefined") {
				svgDraw.line(point1.x, point1.y, point2.x, point2.y, {stroke: STROKE_COLOR, strokeWidth: STROKE_WIDTH})			
			}
			point1 = point2;
		}	
	}
	var count_res = pointsResult.length;
	if (count_res > 0) {
		var point_res = [];
		j = 0;	
		for (i in pointsResult.items) {
			point_res = pointsResult.getItem(i);
			for (i in point_res) {
				point1 = point_res[i];
				j = parseInt(i) + 1;
				point2 = point_res[j];
				if (typeof(point2) != "undefined") {
					svgDraw.line(point1.x, point1.y, point2.x, point2.y, {stroke: STROKE_COLOR, strokeWidth: STROKE_WIDTH})			
				}
			}
		}		
	}
}
// создание квадрата на пересечении линий
function drawRect(point) {
	$("#video").append("<div class='rect' id='" + point.x + "x"+ point.y + "x" + point.number + "'></div>");
	var rect = $("#video div.rect:last");
	rect.css("left", point.x - rect.width() / 2 + "px");
	rect.css("top", point.y - rect.height() / 2 + "px");
	rect.click(function() {
		activeRect($(this));
	});
	rect.mouseover(function() {
		$(this).addClass("rect_over");
	});
	rect.mouseout(function() {
		$(this).removeClass("rect_over");
	});	
}
// выделить квадрат
function activeRect(obj) {
	if (obj.attr("class").indexOf("rect_act") > -1) {
		hideMenu();
	} else {
		$("#video div.rect").removeClass("rect_act");
		obj.addClass("rect_act");
		showMenu(obj);
	}
}
// показать меню
function showMenu(obj) {
	var id = obj.attr("id");
	var coords = id.split("x");
	var coord_left = coords[0] - obj.width();
	var coord_top = coords[1] - obj.height();
	var win = $("#menu_rect"); 
	var dist = 10;
	var win_width = win.width() + dist;
	var win_height = win.height() + dist;	
	var block_width = $("#video").width();
	var block_height = $("#video").height();
	win.removeClass("menu_rect_right")
	if ((coord_left + win_width) > block_width) {
		coord_left = coord_left - win_width + obj.width() + dist;
		win.addClass("menu_rect_right");
	}
	if ((coord_top + win_height) > block_height) {
		coord_top = block_height - win_height;
	}
	win.css("left", coord_left + "px");
	win.css("top", coord_top + "px");
	win.show();
	var action_delete = win.find("ul li a.action_point_delete");
	var action_create = win.find("ul li a.action_polyline_create");
	action_delete.bind("click", function() {
		removePoint(obj);
		return false;
	});
	action_create.bind("click", function() {
		createPolyLines();
		return false;
	});
}
// скрыть меню
function hideMenu() {
	$("#video div.rect").removeClass("rect_act");
	var win = $("#menu_rect"); 
	var action_delete = win.find("ul li a.action_point_delete");
	var action_create = win.find("ul li a.action_polyline_create");
	action_delete.unbind("click");
	action_create.unbind("click");
	win.hide();
}
// завершить создание ломаной
function createPolyLines() {
	hideMenu();
	//drawLines();
	removeRects();
	addToPointsResult();
	deleteDraw();
	$("#btn_polygon").removeClass("polygon_act");
}
// добавить ломаную в массив-результат
function addToPointsResult() {
	var point = {};
	var coords = {};
	var j = 0;
	for (var i in points.items) {
		point = points.getItem(i);
		coords[j] = {x: point.x, y: point.y};
		j++;
	}
	pointsResult.setItem(pointsResult.length, coords);	
}
// удалить квадраты
function removeRects() {
	$("#video div.rect").remove();
}
// удалить точку
function removePoint(obj) {
	hideMenu();
	obj.remove();
	var number = obj.attr("id").split("x")[2];
	points.removeItem(number);
}
// удалить рисование
function deleteDraw() {
	deleteDrawFuncs();
	clearDrawZone();
}
// удалить функции для рисования
function deleteDrawFuncs() {
	var block_draw = $('#svgdraw');
	block_draw.unbind("click");
}
// очистить полностью нарисованную зону 
function clearDrawZone() {
	points.clear();
	removeRects();
}
// сообщение, если параметры не применены
function errorMessage(show, msg) {
	var error = $("#block_error");
	var message = MESS_ERROR;
	if (msg) message = msg;
	if (show) {
		error.html(message);
		error.slideDown("normal");
		$("html").scrollTop(0);
	} else {
		error.slideUp("normal");
	}
}
function successMessage(show, msg) {
	var success = $("#block_success");
	var message = MESS_SUCCESS;
	if (msg) message = msg; 
	if (show) {
		success.html(message);
		success.slideDown("normal");
		$("html").scrollTop(0);
	} else {
		success.slideUp("normal");
	}
}
// заблокировать часть меню, если настройка с изображения
function blockMenu() {
	blockButtons = true;
	$("ul.menu_camera li").addClass("not_avail");
	$("ul.menu_camera li input").attr("disabled", "disabled");
}
function unBlockMenu() {
	blockButtons = false;
	$("ul.menu_camera li").removeClass("not_avail");
	$("ul.menu_camera li input").attr("disabled", false);	
}