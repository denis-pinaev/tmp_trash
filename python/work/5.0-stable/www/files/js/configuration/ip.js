$(function() {
	showIndicatorWindow(true);
	getIpList();
});
function showIndicatorWindow(show) {
	if (show) $("#block_upload").show()
	else $("#block_upload").hide()
}
function getIpList(sorto, up) {
	query = '';
	if (typeof up != "undefined") query += ';up='+up;
	if (typeof sorto != "undefined") query += ';sorto='+sorto;
	$.ajax({
		url: URL_GET_IP_TABLE,
		type:'POST',
		timeout: 30000,
		dataType: 'json',
		data: 'user_login=' + USER + query,
		success: function(msg) {
			showIndicatorWindow(false);
			obj = eval(msg);
			if (obj && obj.status){
				showError(true, ERR[obj.status]); 
			} else if (obj && (obj.result)) {
				$("#block_table").html(obj['result']);
			}
		},
		error: function() {
			showIndicatorWindow(false);
			showError(true, ERR[4]);
		} 
	});
}

//удаление ip адресов
function DelIpList(ip_list){
	showIndicator(true);
	$.ajax({
		url: URL_DEL_IP,
		type:'POST',
		dataType: 'json',
		data: 'ip_list='+$.toJSON(ip_list) + ';user_login=' + USER,
		success: function(msg) {
			showIndicator(false);
			obj = eval(msg);
			if (obj && obj.status){
				showError(true, ERR[obj.status]); 
			}		
			getIpList(SORTO, UP);
		},
		error: function() {
			showIndicator(false);
			showMessage('<div class="text_error">' + MESSAGE_DELETE4 + '</div>');
		} 
	});
}
function showError(show, msg) {
	if (show) {
		if (msg) $("#error_message").html(msg);
		$("#error_message").show();
	} else {
		$("#error_message").hide();
	}
}
// инициализация функций
function initIP() {
	$("#check_all_ip").click(function() {	
		selectAllRow($(this));
	});
	$("#check_all_ip2").click(function() {
		selectAllRow($(this));
	});
	$("#btn_del").click(function() {
		deleteIP();
	});
	$("#btn_del2").click(function() {
		deleteIP();
	});
	$(".table tr td.td_first input[type=checkbox]").attr("checked", false);
	$(".table tr td.td_first input[type=checkbox]").click(function() {
		selectRow($(this));
	});	
}
function countSelectIP() {
	return $(".table tr td.td_first input[type=checkbox]:checked").size();
}
function countIP() {
	return $(".table tr td.td_first input[type=checkbox]").size();
}
function deleteIP() {
	if (countSelectIP() > 0) {
		showMessageDelete(countSelectIP());
	} else {
		showMessage(MESSAGE_DELETE);
	}
}
// окно для удаления
function showMessageDelete(count) {
	changeWindow({id: 'win_del', txt: MESSAGE_DELETE2 + " (<strong>" + count + "</strong>)?", head: HEAD_DELETE1});
}
// получить список выделенный IP адресов
function getListSelectIP() {
	var ip_list = $(".table tr td.td_first input[type=checkbox]:checked");
	var ip_arr = new Array();
	
	$.each(ip_list, function() {
		ip_arr.push($(this).parent().next().find("label").html());
	});
	return ip_arr;
}
// удаление всех IP адресов
function deleteAllIP() {
	$("#check_all_ip").attr("checked", "checked");
	selectAllRow($("#check_all_ip"));
	showMessageDeleteAll(countIP());
}
function showMessageDeleteAll(count) {
	changeWindow({id: 'win_del', txt: MESSAGE_DELETE3 + "?", head: HEAD_DELETE1});
	var btn_ok = $("#win_del").find(".button80_blue")
	removeEvent(btn_ok, 'click');
	btn_ok.click(function() {
		DelIpList(getListSelectIP());
		closeWindow("win_del");
	});
}
// выделение строки
function selectRow(inp) {
	if (inp.attr("checked")) {
		var count_check = $(".table tr td.td_first input[type=checkbox]").size();
		var count_check_checked = $(".table tr td.td_first input[type=checkbox]:checked").size();
		if (count_check == count_check_checked) {
			$("#check_all_ip").attr("checked", "checked");
			$("#check_all_ip2").attr("checked", "checked");
		}
	} else {
		$("#check_all_ip").attr("checked", false);
		$("#check_all_ip2").attr("checked", false);
	}
}
// выделение всех строк на странице
function selectAllRow(inp_all) {
	var checks = $("table.table tr td.td_first input[type=checkbox]");
	var inp_all2_id = "check_all_ip2";
	if (inp_all.attr("id") == "check_all_ip2") {
		inp_all2_id = "check_all_ip";
	} 
	if (inp_all.attr("checked")) {
		$.each(checks, function(key, value){
			$(this).attr("checked", "checked");
			$("#" + inp_all2_id).attr("checked", "checked");
			selectRow($(this));
		});	
	} else {
		$.each(checks, function(key, value){
			$(this).attr("checked", false);
			$("#" + inp_all2_id).attr("checked", false);
			selectRow($(this));
		});		
	}
}
