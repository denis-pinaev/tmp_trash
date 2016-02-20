var params=[];
// инициализация
function init() {
	loadFacesCount();
	checkFormSearch();
	checkAddRulesSearch();
	$("#list_videos li input[type=checkbox]").click(function() {
		selectedRow($(this));
	});	
	$("#list_videos li div.info div.info_cont").click(function() {
		var inp = $(this).parent().parent().find("input[type=checkbox]");
		if (inp.attr("checked")) inp.attr("checked", false)
		else inp.attr("checked", "checked");
		selectedRow(inp);
	});		
	$("input.check_all").click(function() {
		selectedAllRow($(this));
	});	
}
// получить кол-во лиц и персон для каждого ролика
function loadFacesCount(idi) {
    if (!idi) idi = 1;
    var obj = $("#check"+idi);
    if (obj.size() == 0) return false;
    var id = obj.val();
    if (parseInt(id)) {
		$.ajax({
				type: "POST",
				url: URLS["get_video_faces_count"] + "/" + id,
				data: {},
				dataType: "json",
				success: function(msg){
					if(msg.status){
						if (msg.count_faces > 0){
							$("#count_faces"+id).html("<a href='" + URLS["video_faces"] + "'/" + id + "'>" + MESSAGES["faces_found"] + ": " + msg.count_faces + "</a>");
						}else{
							$("#count_faces"+id).html(MESSAGES["faces_found"] + ": "+msg.count_faces);
						}
						if (msg.count_persons > 0){
							$("#count_persons"+id).html("<a href='" + URLS["video_persons"] + "'/" + id + "'>" + MESSAGES["persons_found"] + ": " + msg.count_persons + "</a>");
						}else{
							$("#count_persons"+id).html(MESSAGES["persons_found"] + ": "+msg.count_persons);
						}
					}
					loadFacesCount(idi+1);
				}, 
				error: function(msg){
					loadFacesCount(idi+1);
				}
		});
    }
}
// проверка добавить ли правила для дат
function checkAddRulesSearch() {
	var block = $("#search_ext");
	if (block.css("display") == "block") {
		if ($("#period_dates").attr("checked")) {
			addRulesDates();
			if ($("#daily").attr("checked")) {
				addRulesTime();
			} else {
				removeRulesTime();
			}
		} else {
			removeRulesDates();
		}
		$("#a_click_filter").html(MESSAGES["hide_adv_search"]);
		$("#a_click_filter").addClass("link_search_bottom")
	} else {
		removeRulesDates()
	}
}
// показать/скрыть расширенный поиск
function showSearch(elem, id_block) {
	var search = $("#" + id_block);
	if (search.css("display") == 'none') {
		search.show();
		$(elem).addClass('link_search_bottom');
		$(elem).html(MESSAGES["hide_adv_search"]);
	} else {
		search.hide();
		$(elem).removeClass('link_search_bottom');
		$(elem).html(MESSAGES["adv_search"]);
	}
}
// текущее время
function getCurrentTime(time1, time2) {
	var date = new Date();
	var hour = date.getHours()
	var minute = date.getMinutes();
	$("#" + time1["hour1"]).val(hour);	
	$("#" + time1["minute1"]).val(minute);
	$("#" + time1["second1"]).val('00');
	if (time2) {
		if (hour == 23) $("#" + time2["hour2"]).val('00');
		else $("#" + time2["hour2"]).val(hour + 1);
		$("#" + time2["minute2"]).val(minute);
		$("#" + time2["second2"]).val('00');
	}
}
// текущая дата
function getCurrentDate(delim, id_beg, id_end) {
	var date = new Date();
	var day = ((String(date.getDate()).length == '1')) ? "0" + date.getDate() : date.getDate();
	var month = ((String(date.getMonth() + 1).length == '1')) ? "0" + (date.getMonth() + 1) : (date.getMonth() + 1);
	var year = date.getFullYear();
	$("#" + id_beg).val(day + delim + month + delim + year);
	if ($("#" + id_end).size() > 0) $("#" + id_end).val($("#" + id_beg).val());
}
// выбор интервала дат
function clickIntervalLable(){
    $("#period_dates").attr("checked", "checked");
	addRulesDates();
}
// выделение всех строк
function selectedAllRow(inp) {
	var checks = $("#list_videos li input[type=checkbox]");
	var checks_all = $("input[type=checkbox].check_all");
	if (inp.attr("checked")) {
		$.each(checks, function() {
			$(this).attr("checked", "checked");
			$(this).parent().addClass("act");
		});
		checks_all.attr("checked", "checked");
	} else {
		$.each(checks, function() {
			$(this).attr("checked", false);
			$(this).parent().removeClass("act");
		});
		checks_all.attr("checked", false);	
	}
}
// выделение одной строки
function selectedRow(inp) {
	var checks_all = $("input[type=checkbox].check_all");
	var count = $("#list_videos li input[type=checkbox]").size();
	var count_sel = 0;
	if (inp.attr("checked")) {
		inp.parent().addClass("act");
		count_sel = $("#list_videos li input[type=checkbox]:checked").size();
		if (count_sel == count) {
			checks_all.attr("checked", "checked");
		}
	} else {	
		inp.parent().removeClass("act");
		checks_all.attr("checked", false);
	}
}
// удалить выделенные
function showMessageDelete() {
	var count_sel = $("#list_videos li input[type=checkbox]:checked").size();
	if (count_sel > 0) {
		changeWindow({id: 'win_del', css: {width: '300px', height: '200px'}, txt: replace_string(MESSAGES["delete"], '{}', count_sel)});
	} else {
		changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: ERRORS["no_data"]});
	}
}
// получить значения выделенных видеороликов
function clickDelete(count) {
	closeChangeWindow('win_del');
	var obj = getValueIsChecked(count);
	var res = '';
	for(var i = 0; i<obj.c; i++) {
		if (i!=0){
			res=res+',';
		}
		res = res + obj.array[i];
	}
	return res;
}
function getValueIsChecked(count) {
	var c = 0;
	var arr_value = new Array();
	if (count > 0) {
		var inps = $("#list_videos li input[type=checkbox]:checked");
		$.each(inps, function() {
			arr_value[c] = $(this).val();
			c++;
		});
	}
	return {c: c, array: arr_value};
}
// функция на удаление
function del(rollers) {
	closeChangeWindow('win_del');
    showIndicator(true);
    $.ajax({
        type: "POST",
        url: URLS["video_delete"],
        data: {rollers: rollers},
        success: function(msg){
			showIndicator(false);
            setTimeout('location.reload(true)', 1000);
        },
        error: function(msg){
            setTimeout('location.reload(true)', 1000);
        }
    });
}
// экспорт видеороликов
function saveOriginalVideo() {
	var count_sel = $("#list_videos li input[type=checkbox]:checked").size();
	if (count_sel > 0) {
		changeWindow({id: 'win_save_orig', css: {width: '300px', height: '200px'}, txt: replace_string(MESSAGES["export"], '{}', count_sel)});
	} else {
		changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: ERRORS["no_data"]});
	}
}
// удалить найденные
function showMessageAllDelete(count) {
	changeWindow({id: 'win_all_del', css: {width: '300px', height: '200px'}, txt: replace_string(MESSAGES["delete_found"], '{}', count)});
}
function deleteAllRollers() {
	closeChangeWindow('win_all_del');
	showIndicator(true);
	var options = {	  
		url: URLS["video_delete_found"],	  
		success: function(msg) {
			showIndicator(false);
			if (msg && msg.status){
				showMessage(MESSAGES["video_delete_found"]);
				setTimeout('location.reload(true)', 1000);
			}else{
				showMessage(ERRORS["video_delete_found"]);
			}
		},
		error: function(msg) {
			showIndicator(false);
			showMessage(ERRORS["video_delete_found"]);
		}
	};
	$("#main_form").ajaxSubmit(options);
}