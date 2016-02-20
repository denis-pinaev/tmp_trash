var params = new Array(); // массив значений, формируется при загрузке страницы
// функция, которая нужна для того, чтобы сформировать hash-массив
function Hash() {
	this.length = 0;
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
var hashArray = new Hash();
$(document).ready(function(){
	init();
});
// инициализация 
function init() {
	initTooltip();
	initFuncs();
}
// инициализация всплыв подсказки
function initTooltip() {
	$("#detectors #block_sensors div input[type=button]").easyTooltip();
	$("#detectors #block_sensors div .detector").easyTooltip();	
}
// инициализация функций
function initFuncs() {
	$(".form .form_block .fb_content select").blur(function() {
		activeBlock($(this), false);
	});
	$(".form .form_block .fb_content select").focus(function() {
		activeBlock($(this), true);
	});	
	
	$(".form .form_block .fb_content input[type=text]").blur(function() {
		activeBlock($(this), false);
	});
	$(".form .form_block .fb_content input[type=text]").focus(function() {
		activeBlock($(this), true);
	});	

	$(".form .form_block .fb_content .spinbox .spinbtns input[type=button]").blur(function() {
		activeBlock($(this).parent().prev(), false);
	});
	$(".form .form_block .fb_content .spinbox .spinbtns input[type=button]").focus(function() {
		activeBlock($(this).parent().prev(), true);
	});	

	$("#detectors #block_sensors input.settings_detector_btn").click(function() {
		settingsDetector($(this));
	});	
	$("#btnForm2").click(function() {
		bgGeneration();
	});
}
//сделать камеру активной
function activeCamera(obj_link) {
	var block = obj_link.parent();
	if (block.attr("class").indexOf("noact") < 0) {
		initListCameras();
		block.addClass("act");
	}
}
function initListCameras() {
	$("#cameras div.camera").removeClass("act");
}
// выделение текущего блока
function activeBlock(obj, active) {
	var block = getBlock(obj, "form_block");
	if (active) {
		block.addClass("active_block")
		if (obj.attr("class").indexOf("error") < 0) {
			obj.addClass("active");
		}
	} else {
		block.removeClass("active_block");
		obj.removeClass("active");
	}
}
// получение объекта с указанным классом
function getBlock(obj, class_name) {
	var parentObj = obj;
	var parentCls;
	while (parentObj) {
		parentCls = parentObj.attr("class");
		if (parentCls && (parentCls.indexOf(class_name) > -1)) {
			return parentObj;
		}
		parentObj = parentObj.parent();
	}
}
// показать настройки детектора
function settingsDetector(obj) {
	var id_block = obj.attr("name");
	var block = $("#" + id_block);
	if (block.css("display") == "none") {
		$(".settings_detector").hide();
		block.slideDown("normal");
	} else {
		block.slideUp("normal");
	}
}
// сгенерировать фон
function fonDetector() {
	updateBGGenStartTime();
	changeWindow2({
		id: "win_genfon", 
		head: HEAD_WINDOW,
		css: { "width": "700px", "height": "585px" }
	});
}
// сообщение, если параметры успешно применены
function successMessage(show, msg) {
	 var message = MESS_SUCCESS;
	 if (msg) {
	  message = msg;
	 } 
	 if (show) {
	  $("#success_message").html(message);
	  $("#success_message").slideDown("normal");
	  $("html").scrollTop(0);
	 } else {
	  $("#success_message").slideUp("normal");
	 }
	}
	// сообщение, если параметры не применены
	function errorMessage(show, msg) {
	 var message = MESS_ERROR;
	 if (msg) {
	  message = msg;
	 } 
	 if (show) {
	  $("#error_message").html(message);
	  $("#error_message").slideDown("normal");
	  $("html").scrollTop(0);
	 } else {
	  $("#error_message").slideUp("normal");
	 }
	}
// проверка на изменение значений в полях ввода
function checkValueChange(obj) {
	var value = obj.attr("value");
	if (obj.attr("type") == "checkbox") {
		if (obj.attr("checked")) { value = "checked"; } else { value = "false"; }
	}
	if (params[obj.attr("id")] != value) {
		hashArray.setItem(obj.attr("id"), value);
		activeButton(true);	
	} else {
		hashArray.removeItem(obj.attr("id"));
		activeButton(false);	
	}
}
// изменение значений параметров в глобальном массиве и очищение hash-массива
function changeGlobalParams() {
	for (var i in hashArray.items) {
		params[i] = hashArray.items[i];
	}
	hashArray.clear();
}
// делать кнопку активной или неактивной в зависимости от того, есть ли изменения
function activeButton(active) {
	if (active) {
		$("#btnForm").removeClass("noact_btn");
		$("#btnForm").attr("disabled", false);
	} else {
		if (hashArray.length == 0) {
			$("#btnForm").addClass("noact_btn");
			$("#btnForm").attr("disabled", "disabled");
		}
	}
}
function hideSettings(id) {
	var inps = $("#" + id).find("div.spinbox input[type=text].inp_txt");
	if (inps.size() > 0) {
		$.each(inps, function() {
			$(this).val(params[$(this).attr("id")]);
		});
	}
	$("#" + id).slideUp("normal");
}
function setValueGlobalParams(id) {
	var inps = $("#" + id).find("div.spinbox input[type=text].inp_txt");
	if (inps.size() > 0) {
		$.each(inps, function() {
			params[$(this).attr("id")] = $(this).val();
		});
	}
}