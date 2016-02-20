$(document).ready(function(){
	init();
});
function init() {
	$("#link_add_photos").click(function() {
		showMenuPhotos($(this));
		return false;
	});
}
function showMenuPhotos(link) {
	if (link.attr("class").indexOf("dis") > -1) {
		return;
	} else {
		var menu = link.next();
		if (menu.css("display") == "none") {
			menu.slideDown("normal");
		} else {
			menu.slideUp("normal");
		}
	}
}
// �������� ������ ����
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
// �������� ���������� ������� ���
function checkDateRangeValidator(id_start, id_stop) {
	var objStart = $("#" + id_start).val().split(".");
	var objStop = $("#" + id_stop).val().split(".");
	var strStart = get_DateString(objStart);
	var strStop = get_DateString(objStop);
	var intStart = Date.parse(strStart);
	var intStop = Date.parse(strStop);
	return [intStart, intStop];
}
// ����� ���������
function chooseDoc() {
	var text = $("#document option:selected").text();
	if (text == PASSPORT) {		
		addRulesDocumentPassport();
	} else {
		$("#passport_series").attr("maxlength", 8);
		$("#passport_number").attr("maxlength", 16);	
		removeRulesDocumentPassport();
	}
}
// функции на проверку корректности ФИО
function addFuncsNameValid() {
	$("#first_name").bind("keyup click", function() {
		isNameValid($(this));		
	});
	$("#last_name").bind("keyup click", function() {
		isNameValid($(this));		
	});	
	$("#middle_name").bind("keyup click", function() {
		isNameValid($(this));		
	});		
}
// проверить имя
function isNameValid(element) {
	var value = $.trim(element.attr("value"));
	var block = element.next();
	
	if (value) {
		var reg = /^\s*[a-zA-Zа-яА-ЯёЁ-]+(\s+[a-zA-Zа-яА-ЯёЁ-]+)*\s*$/;
		
		if (reg.test(value)) {
			block.html("");
			element.removeClass("border_warning");
		} else {
			block.html(setMessageWarning(element))
			element.addClass("border_warning");
		}
		
	} else {
		block.html("");
		element.removeClass("border_warning");
	}
}
// предупреждение о некорректности имени
function setMessageWarning(element) {
	var id = element.attr("id");
	if (id == "first_name") {
		return WARNING["surname"];
	} 
	if (id == "last_name") {
		return WARNING["name"];
	} 
	return WARNING["patronymic"];
}
// проверка при загрузке страницы на валидность ФИО
function isSavedNameValid() {
	isNameValid($("#first_name"));
	isNameValid($("#last_name"));
	isNameValid($("#middle_name"));
}