function runStrFunc(func) {
    eval(func);
}
function sendCommand(command, param, retFunc){
	executeMethod({"command":command, "param":param}, retFunc)
}
function executeMethod(params, retFunc){
    var d = params;
    $.ajax({
            type: "GET",
            url: "/settings/turnstiles/command/",  //Необходимо сделать именнованым урлом
            data: d,
            success: function(data){
                retFunc(data);
            }
    });
}
function init() {
	initTooltip();
	funcsTable();
	//funcsCameras();
}
function funcsTable() {
	$("input.check_all").click(function() {
		selectedAllRow($(this));
	});
	$("#table tr").mouseover(function() {
		overRow($(this))
	});	
	$("#table tr").mouseout(function() {
		outRow($(this))
	});
	$("#table tr td input[type=checkbox].inp_check").click(function() {
		selectedRow($(this));
	});	
}
// выделить все строки
function selectedAllRow(inp) {
	var checks = $("#table td input[type=checkbox]");
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
// выделить строку
function selectedRow(inp) {
	var checks_all = $("input[type=checkbox].check_all");
	var count = $("#table tr td input[type=checkbox]").size();
	var count_sel = 0;
	if (inp.attr("checked")) {
		count_sel = $("#table tr td input[type=checkbox]:checked").size();
		if (count_sel == count) {
			checks_all.attr("checked", "checked");
		}
	} else {	
		checks_all.attr("checked", false);
	}
}
// видео с камеры
function funcsCameras() {
	$("a.set_camera").mouseover(function() {
		showInfoCamera($(this));
	});
	$("a.set_camera").mouseout(function() {
		hideInfoCamera();
	});
}
// показать окно для видео с камеры
function showInfoCamera(obj) {
	$("#camera_name").html(obj.html());    
	createTitleWindow2({id: "easyTooltip_camera", obj: obj, width: 200, height: 200, distY: -15});
	getVideoInfo("camera_frame");
}
function hideInfoCamera() {
	$("#easyTooltip_camera").hide();
}
// всплывающие подсказки
function createTitleWindow2(param) {
    var distX = param.distX ? param.distX : 0; 
    var distY = param.distY ? param.distY : 0; 
    var win = $("#" + param.id);   
	var pos_win = param.obj.offset();
    var coord_left = pos_win.left + param.obj.width() + "px";
    var coord_top = pos_win.top + param.obj.height() + "px";
    win.css("left", coord_left);
    win.css("top", coord_top);
	if (param.txt) {
		$("#" + param.id).html(param.txt);
	}
    win.show();
}
function getVideoInfo(block_id) {
	var img = $("#"+block_id+" img");
	img.attr("src", "/files/images/photo_example.jpg");
}
// Удаление турникетов
function deleteTurnstiles() {
	var count_checks = $("#table tr td input[type=checkbox]:checked").size();
	if (count_checks > 0) {
		changeWindow({id: 'win_del', css: {width: '300px', height: '200px'}, txt: replace_string(MESSAGES["delete"], '{}', count_checks)});
	} else {
		showMessage(MESSAGES['warning']);
	}
}
function deleteSelectedTurns(){
	closeChangeWindow('win_del');
	showIndicator(true);
	var checks = $("#table tr td input[type=checkbox]:checked")
	var count_checks = checks.size();
	var delstr = ''
	for (var i=0;i<count_checks;i++){
		delstr+=checks[i].id
		if(i<count_checks-1) delstr+=',';
	}
	sendCommand('delete',delstr,fromDelete);
}
function fromDelete(data){
	showIndicator(false);
	if (data.status) {
		var delturns = data.param.split(',');
		if ($("#table tr:not(:first)").size() > delturns.length) {
			var tarr = data.deleted;
			var ids = new Array();
			var ips = new Array();
			for (var i=0; i<tarr.length; i=i+2){
				ids[i/2] = tarr[i];
				ips[i/2] = tarr[i+1];
			}	
			addTurnsFromSearchTable(ids, ips);
			deleteTurnsFromTable(ids);
			updateCountTurns($("#table tr:not(:first)").size());
		} else {
			window.location.reload();
		}
	}else{
		showMessage(MESSAGES['warning']);
	}
}
// удаление строк из таблицы
function deleteTurnsFromTable(ids) {
	var tr;
	for (var i = 0; i < ids.length; i++) {
		tr = $("#" + ids[i]).parent().parent();
		tr.remove();
	}
}
// добавление строк в форму поиска
function addTurnsFromSearchTable(ids, ips) {
	return;
	/*var block = $("#list_search_turnstiles");
	var li;
	var tr;
	for (var i = 0; i < ids.length; i++) {
		tr = $("#" + ids[i]).parent().parent();
		if (tr.attr("class").indexOf("tr_lock") < 0) {
			li = '<li><input name="" value="" id="search_turnstile' + ids[i] + '" type="checkbox" class="inp_check" onClick="javascript: selectedRowSearch($(this));" /><label for="search_turnstile' + ids[i] + '">' + ips[i] + '</label></li>';
			block.append(li);
		}		
	}
	initSearchTableTurns();*/
}
// текущее состояние кнопки включения
function checkSwitch(obj) {
	if (obj.attr("class") && (obj.attr("class").indexOf("off") > -1)) {
		return "off";
	} else { 
		return "on";
	}
}
// вкл./выкл. турникет
function onOffTurn(btn, id, name) {
	var state = checkSwitch(btn)
	showIndicator(true);
	state = (state=="on")?"off":"on";
	sendCommand(state, id, fromChange);
}
function fromChange(data){
	showIndicator(false);
	if (data.status) {
		var btn = $("#btn_turn" + data['param']);
		var name = btn.next().html();
		if (data['command'] == "on") {
			btn.removeClass("off");
			btn.addClass("on");			
		} else {
			btn.removeClass("on");
			btn.addClass("off");		
		}
		$("#easyTooltip_turnstile").html(name + " <strong>" + MESSAGES[data.command] + "</strong>");
	}else{
		showMessage(MESSAGES['error']);
	}
}
// всплывающая подсказка на кнопку Вкл./Выкл. камеру
function overSwitchTurn(btn, name) {
	var state = checkSwitch(btn);
	state = name + " <strong>" + MESSAGES[state] + "</strong>";
	createTitleWindow2({id: "easyTooltip_turnstile", obj: btn, txt: state });
}
function outSwitchTurn() {
	$("#easyTooltip_turnstile").hide();
}
// поиск турникетов
function searchTurnstiles(){
	showIndicator(true);
	sendCommand("new", "new", fromNewTurns);
}
//server response abt new turns
function fromNewTurns(data){
	showIndicator(false);
	if (data.status) {
		var new_turns = data.new_turns;
		var block = $("#list_search_turnstiles");
		block.empty();
		//if(new_turns.length == 0) new_turns = [{'id':123, 'address':'test.address'}, {'id':124, 'address':'test2.addr'},{'id':125, 'address':'trrr.address'}, {'id':126, 'address':'teeee.aaaa'}];
		for(var i=0; i<new_turns.length; i++){
			li = '<li><input name="" value="" id="search_turnstile' + new_turns[i].id + '" type="checkbox" class="inp_check" onClick="javascript: selectedRowSearch($(this));" /><label for="search_turnstile' + new_turns[i].id + '">' + new_turns[i].address + '</label></li>';
			block.append(li);
		}
		initSearchTableTurns();
		checkTurnstiles();
	}else{
		showMessage(MESSAGES['error']);
	}
}

function checkTurnstiles() {
	var count_search = $("#list_search_turnstiles li").size();
	if (count_search > 0) {
		var check_all = $("#choose_all_search");
		check_all.attr("checked", false);
		selectedAllRowSearch(check_all);
		$("#count_search").html(count_search);
		changeWindow2({id: 'win_search', css: {width: '400px', height: '300px'}});
	} else {
		showMessage(MESSAGES['search']);
	}
}
// выделить все записи для поиска
function selectedAllRowSearch(inp) {
	var checks = $("#list_search_turnstiles li input[type=checkbox]");
	if (inp.attr("checked")) {
		$.each(checks, function() {
			$(this).attr("checked", "checked");
		});
	} else {
		$.each(checks, function() {
			$(this).attr("checked", false);
		});	
	}
	setValueErrorAddTurns("");
}
// выделить одну запись поиска
function selectedRowSearch(inp) {
	var check_all = $("#choose_all_search");
	var count = $("#list_search_turnstiles li input[type=checkbox]").size();
	var count_sel = 0;
	if (inp.attr("checked")) {
		count_sel = $("#list_search_turnstiles li input[type=checkbox]:checked").size();
		if (count_sel == count) {
			check_all.attr("checked", "checked");
		}
	} else {	
		check_all.attr("checked", false);
	}
	setValueErrorAddTurns("");
}
// добавление турникетов
function addTurns() {
	var checks = $("#list_search_turnstiles li input[type=checkbox]:checked");
	if (checks.size() > 0) {
		closeChangeWindow('win_search');
		var ids = new Array();
		var ips = new Array();
		var i = 0;
		$.each(checks, function() {
			ids[i] = $(this).attr("id");
			ips[i] = $(this).next().html();
			i++;
		});
		sendstr = ''
		for (i=0;i<ids.length;i++){
			sendstr += ids[i].split('search_turnstile')[1]+','+ips[i]
			if(i<ids.length-1){
				sendstr += ','
			}
		}
		showIndicator(true);
		sendCommand("add", sendstr, fromAdd);		
	} else {
		setValueErrorAddTurns(MESSAGES['add']);
	}
}
// установить ошибку при добавлении турникетов
function setValueErrorAddTurns(text) {
	var error = $("#error_add_turns");
	error.html(text);
}
// ответ от сервера на добавление
function fromAdd(data){
	showIndicator(false);
	if (data.status && data.added) {
		if ($("#table").size() > 0) {
			var tarr = data.added;
			var ids = new Array();
			var ips = new Array();
			for (var i=0; i<tarr.length; i=i+2){
				ids[i/2] = tarr[i];
				ips[i/2] = tarr[i+1];
			}
			addTurnsToTable(ids, ips);
			removeTurnsFromSearchTable(ids, ips);
			updateCountTurns($("#table tr:not(:first)").size());
		} else {
			window.location.reload();
		}
	}else{
		showMessage(MESSAGES['error']);
	}
}
// добавление турникетов в таблицу
function addTurnsToTable(ids, ips){
	var tr;
	for (var i = 0; i < ids.length; i++) {
		tr = createTR(ids[i], ips[i]);
		$("#table tr:first").after(tr);
	}
	initTableTurns();
}
// создание строки
function createTR(id, ip) {
	var html = '<tr>';
	html += '<td class="first"><input type="checkbox" name="" value="" class="inp_check" id="' + id + '"/></td>';
	html += '<td class="td_id">' + id + '</td>';
	html += '<td><input type="button" name="" value="" id="btn_turn' + id + '" class="btn_turn on" onClick="javascript: onOffTurn($(this), \'' + id + '\', \'' + ip + '\');" onMouseOver="javascript: overSwitchTurn($(this), \'' + ip + '\');" onMouseOut="javascript: outSwitchTurn();" /><a href="/turnstiles/edit/?id=' + id + '">' + ip + '</a></td>';
	html += '<td>&nbsp;</td>';
	html += '<td>&nbsp;</td>';
	html += '<td>&nbsp;</td>';
	html += '</tr>';
	return html;
}
// инициализация таблицы турникетов
function initTableTurns() {
	$("#table tr.odd").removeClass("odd");
	$("#table tr:not(.tr_lock):odd").addClass("odd");
}
// удаление добавленных турникетов из формы поиска
function removeTurnsFromSearchTable(ids, ips) {
	var li;
	for (var i = 0; i < ids.length; i++) {
		li = $("#search_turnstile" + ids[i]).parent();
		li.remove();
	}
	initSearchTableTurns();
}
// инициализация формы поиска
function initSearchTableTurns() {
	var count = $("#list_search_turnstiles li").size();
	if (count > 0) {
		$("#list_search_turnstiles li.odd").removeClass("odd");
		$("#list_search_turnstiles li:odd").addClass("odd");	
	}
}
function updateCountTurns(count) {
	$("#count_turns").html(count);
}