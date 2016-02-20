// инициализация
function init() {
	updateTime(0);
	setLocationContent();
	stateButtons();
	checkForm();
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
	$("#body1").css("margin-top", getMarginTop());
}
// получить отступ по вертикале
function getMarginTop() {
	var scr = getScreenSize();
	var body = $("#body1");
	var height = body.height();
	var footer = $("#footer");
	var margin_top = 0;
	if (scr.height > height) {
		margin_top = parseInt( (scr.height - height) / 2 ) - footer.height();
	}
	return margin_top + "px"
}
// общие функции для отображения состония кнопок (normal, over, pressed)
function stateButtons() {
	$(".button").mouseover(function() {
		$(this).removeClass("normal");
		$(this).addClass("over");
	});
	$(".button").mouseout(function() {
		$(this).removeClass("over");
		$(this).addClass("normal");
	});	
	$(".button").mousedown(function() {
		$(this).addClass("pressed");
	});		
	$(".button").mouseup(function() {
		$(this).removeClass("pressed");
	});		
}
// проверка формы на валидность введённых значений
function checkForm() {
	$.validator.addMethod("checkLogin", function(value, element) {
		var value = $(element).attr("value");
		var reg = /^[a-zA-Z0-9_]{3,30}$/;
		if (reg.test(value)) return true;
		return false;
	}, "Введено некорректное значение" );			
	var validator = $("#frm_login").validate({
		rules: {
			login: {
				required: true,				
				minlength: 3,
				checkLogin: true		
			},
			password: {
				required: true,
				minlength: 6					
			}
		},
		messages: {
			login: {
				required: VALIDATOR["username"]["required"],
				minlength: VALIDATOR["username"]["minlength"],
				checkLogin: VALIDATOR["username"]["checkLogin"]
			},
			password: {
				required: VALIDATOR["password"]["required"],
				minlength:  VALIDATOR["password"]["minlength"]
			}
		},
		errorPlacement: function(error, element) {
			error.appendTo( element.parent().parent().prev() ); 
		}		
	});		
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