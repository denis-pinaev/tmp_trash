var MIN_HEIGHT = 748; // минимальная высота окна браузера (уменьшили на 20px из-за заголовка на ipad)
var MIN_WIDTH = 1024; // минимальная ширина окна браузера

var INTERVAL_UPDATE = 1000; // обновление данных
 
// инициализация
function init() {
	updateTime(0);
	firstUpdateData();
	stateButtons();
	setLocationContent();
	$(window).resize(function() {
		setLocationContent();
	});	
}
// получить размер экрана
function getScreenSize() {
	return { width: $(window).width(), height: $(window).height() }
}
// выровнить блок с контентом по вертикали
function setLocationContent() {
	var scr = getScreenSize();
	var body = $("#body1");
	if (scr.height > MIN_HEIGHT) {
		var padding_top = parseInt( (scr.height - body.height()) / 2 );
	} else {
		var padding_top = 0;
	}
	
	body.css("padding-top", padding_top + "px");
}
// общие функции для отображения состония кнопок (normal, over, pressed)
function stateButtons() {
	$(".button").mouseover(function() {
		$(this).addClass("over");
	});
	$(".button").mouseout(function() {
		$(this).removeClass("over");
	});	
	$(".button").mousedown(function() {
		$(this).addClass("pressed");
	});		
	$(".button").mouseup(function() {
		$(this).removeClass("pressed");
	});		
}
// выход или смена оператора
function exit() {
	window.location.href = '/logout';
}
// текущее время
// получить двухзначное число
function getDoubleNumber(num) {
	if (num > 9){
		return num;
	} else {
		return '0' + num;
	}
}
// сформировать время
function makeCurrentTime() {
	return getDoubleNumber(hour) + ':' + getDoubleNumber(minute) + ':' + getDoubleNumber(second);
}
// обновлять время
var ms = 0;
function updateTime(add) {
	ms += add;
	while (ms >= 1000) {
		second += 1;
		ms -= 1000;
	}
	while (second >= 60) {
		minute += 1;
		second -= 60;
	}
	while (minute >= 60) {
		hour += 1;
		minute -= 60;
	}
	while (hour > 24) {
		hour -= 24;
	}
	if ($("#current_time").size() > 0) {
		$("#current_time").html(makeCurrentTime());
		setTimeout('updateTime(500);', 500);
	}
}
// обновление данных
function updateData(id, action) {
	var curr_person = $("#id_current_person").val(); // id текущей персоны
	var id_agregate = $("#id_agregate").val();         // id записи в журнале
	var query_str = "";

	if (id_agregate) {
		query_str += "&agregate_id=" + id_agregate;
    }
    
	if (id) {
	    query_str += "&id=" + id;
		if (action) {
			query_str += "&action=" + action; 
		}
	}
	
	if (curr_person){
		query_str += "&id_person=" + curr_person;
	}
	$.ajax({
		type: "GET",
		url: URLS["security"] + "?data=true" + query_str,
		data: {},
		success: function(msg){
			setData(msg);
			id_journal = $("#id_journal").val();
			if (id_journal == "0") {
				setTimeout("updateData()", INTERVAL_UPDATE);
			}
			stateButtons();
			
		},
		error: function(msg) {
			setTimeout("updateData()", INTERVAL_UPDATE);
			stateButtons();
		}
	});
	return false
}
// установить данные
function setData(msg) {
	var data = $("#dataSecurity");
	data.html(msg);
	return false;
}
// обновление данных при загрузке страницы
function firstUpdateData() {
	var id_journal = $("#id_journal").val();
	if (id_journal == "0"){
		updateData();
	}
}
// сбросить данные
function resetData() {
	$("#FormIds").submit();
}
// окно с предупреждением
function showWarning(id, text) {
	$( "#" + id ).find("div.block_msg div.text").html(text);
	$( "#" + id ).dialog({
		modal: true,
		resizable: false,
		draggable: false,
		width: 400,
		buttons: [
			{
				text: BUTTONS["ok"],
				click: function() { $(this).dialog("close"); }
			}
		],
		open: function(event, ui) {
			var header = $(this).prev();
			header.addClass("warning");
			var close = header.find("span.ui-icon-closethick");
			close.addClass("white");
		}
	});			
}