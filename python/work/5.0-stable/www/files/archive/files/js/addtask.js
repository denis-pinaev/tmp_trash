// Инициализация
function init() {
	checkForm();
	initTooltip();
	funcsElementsForm();
	funcsCameras();
	funcsSignals();
	funcsRepeat();
	funcsAdvancedParams();
	initForm();	
	initRulesForm();
}
function initForm(){
    $("#frm_add_task").change(function(){
        getNote();
    });
    $("#frm_add_task").keyup(function(){
        getNote();
    });
	getNote();
}
function initTooltip() {
	$(".short_descr").easyTooltip();
}
// общие функции для формы
function funcsElementsForm() {
	initFirstElementForm();
	$(".el_enter").mouseover(function() {
		//$(this).addClass("inp_over");
	});
	$(".el_enter").mouseout(function() {
		//$(this).removeClass("inp_over");
	});
}
// инициализация первого элемента формы
function initFirstElementForm() {
	$("#name").focus();
	//$("#name").addClass("inp_over");
}
// функции для камеры
function funcsCameras() {
	$("#list_cameras li label").mouseover(function() {
		var li = $(this).parent();
		li.addClass("lc_over");
		if (li.attr("class").indexOf("lc_dis") < 0) {	
			showInfoCamera($(this));
		}
	});
	$("#list_cameras li label").mouseout(function() {
		var li = $(this).parent();
		li.removeClass("lc_over");
		if (li.attr("class").indexOf("lc_dis") < 0) {
			hideInfoCamera();
		}
	});
	$("#list_cameras input[name=source]").click(function() {
		selectedCamera($(this));
	});
	$("#list_cameras li span").mouseover(function() {
		$(this).parent().addClass("lc_over");
	});	
	$("#list_cameras li span").mouseout(function() {
		$(this).parent().removeClass("lc_over");
	});
	checkSelectedCamera();
	getResolution();
}
// изображение с камеры
function showInfoCamera(obj) {
	var param_cam = eval('(' + obj.next().val() + ')');
    $("#camera_name").html(param_cam['info']);  
	createTitleWindow({id: "easyTooltip_camera", obj: obj, width: 200, height: 200, distY: -15});
    getVideoInfo("camera_frame", obj.attr("id"));	
}
function hideInfoCamera() {
	$("#easyTooltip_camera").hide();
}
// выбранная камера
function selectedCamera(inp) {
	$("#list_cameras li").removeClass("lc_act");
	inp.parent().addClass("lc_act");
}
// проверка выбрана ли камера
function checkSelectedCamera() {
	var inp = $("#list_cameras li input[name=source]:checked");
	if (inp.size() > 0) {
		inp.parent().addClass("lc_act");
	}
}
// получить значение активной камеры
function getValueActiveCamera() {
	return $("#list_cameras li input[name=source]:checked").attr("value");
}
// видео с камеры
function createTitleWindow(param) {  
    var distX = param.distX ? param.distX : 0; 
    var distY = param.distY ? param.distY : 0; 
    var win = $("#" + param.id);   
    var pos_win = positionScreen2({obj: param.obj, win_width: parseInt(win.css("max-width")), win_height: parseInt(win.css("max-height")), distX: distX, distY: distY});
    var coord_left = pos_win.left + "px";
    var coord_top = pos_win.top + "px";
    win.css("left", coord_left);
    win.css("top", coord_top);
    win.show();
}
function positionScreen2(param) {
	var elem = param.obj;
	var pos_elem = elem.offset();
	var top = pos_elem.top - param.distY;
	var left = pos_elem.left + elem.width() + param.distX;
	var scr = screenSize();
	if ( ( left + param.win_width ) > scr.width ) {
		left = pos_elem.left - param.win_width - param.distX;
	}
	if (param.win_height) {
		if ( ( top + param.win_height ) > scr.height ) {
			top = scr.height - param.win_height - param.distY;
		}
	}
	return { top: top, left: left };
}
// функции для сигналов
function funcsSignals() {
	$("input[name=signal_type]").click(function() {
		selectedSignal($(this));
	});
	$("#list_detectors li").mouseover(function() {
		$(this).addClass("det_over");
	});
	$("#list_detectors li").mouseout(function() {
		$(this).removeClass("det_over");
	});	
	$("#list_detectors li input[type=radio]").click(function() {
		selectedDetector($(this));
	});
	$("#list_detectors li a").click(function() {
		var inp = $(this).prev();
		if (inp.attr("checked")) inp.attr("checked", false)
		else inp.attr("checked", "checked")
		selectedDetector(inp);
		return false;
	});
}
// выбранный сигнал
function selectedSignal(inp) {
	var id = inp.attr("id");
	if (id == "record_detectors") {
		$("#list_detectors").slideDown("fast");
		//$("#list_detectors li").addClass("det_noact");
		$("#signal_simple").attr("checked", false);
		initTooltip();
		addRulesDetectors();
	} else {
		$("#list_detectors").slideUp("fast");
		$("#list_detectors li").addClass("det_noact");
		setSimpleSignal();
		$("#error_signal").html("");
		removeRulesDetectors()
	}
}
// выбрать детектор
function selectedDetector(inp) {
	if (inp.attr("checked")) {
	    $("#list_detectors li input[type=radio]").attr("checked", false);
		$("#list_detectors li").addClass("det_noact");
		inp.parent().removeClass("det_noact");
	    inp.attr("checked", "checked");
		$("#error_signal").html("");
	} else {
	    inp.parent().addClass("det_noact");	    
	}
}
// функции для блока повторений
function funcsRepeat() {
	$("input[name=repeat_task]").click(function() {
		blockRepeat($(this));
	});
	$("#all_day").click(function() {
		checkAllDay($(this));
	});
	$("#repeat_select").change(function() {
		showBlockDays();
		checkInterval($(this).val());
	});
	$("#repeat_start_date").change(function() {
		getNote();
	});
	$("#repeat_stop_date").change(function() {
		getNote();
	});		
	$("input[name=interval]").click(function() {
		if ($(this).attr("id") == "repeat_interval_record") {
			$("#repeat_stop_date").removeClass("inp_txt_dis");
			addRulesBlockRepeatDateStop();
		} else {
			$("#error_repeat_stop_date").html("");
			$("#repeat_stop_date").removeClass("err_forms");
			$("#repeat_stop_date").addClass("inp_txt_dis");
			removeRulesBlockRepeatDateStop();
		}
	});
	$("#repeat_stop_date").click(function() {
		$("#repeat_interval_record").attr("checked", "checked");
		$(this).removeClass("inp_txt_dis");
		getNote();
		addRulesBlockRepeatDateStop();
	});	
	$("#repeat_stop_date_calend").click(function() {
		$("#repeat_interval_record").attr("checked", "checked");
		$("#repeat_stop_date").removeClass("inp_txt_dis");
		getNote();
		addRulesBlockRepeatDateStop();
	});	
	$("#repeat_list_days li input[type=checkbox]").click(function() {
		selectRepeatDays($(this));
	});
	$("#repeat_list_days li").mouseover(function() {
		$(this).addClass("over_day");
	});	
	$("#repeat_list_days li").mouseout(function() {
		$(this).removeClass("over_day");
	});		
	initBlockRepeat(); // если новая задача
}
// блок для повторения
function blockRepeat(inp) {
	if (inp.attr("id") == "repeat_task_yes") {
		$("#bl_repeat_task_no").hide();
		$("#bl_repeat_task_yes").slideDown("fast");
		$("#time_start").rules("remove");
		$("#time_stop").rules("remove");
		removeRulesBlockNoRepeat();
		addRulesBlockRepeat();
	} else {
		$("#bl_repeat_task_yes").hide();
		$("#bl_repeat_task_no").slideDown("fast");
		checkDuration();
		$("#repeat_start_time").rules("remove");
		$("#repeat_stop_time").rules("remove");
		$("#duration").rules("remove");
		removeRulesBlockRepeat();
		addRulesBlockNoRepeat();
	}
}
// показать блок с выбором дней
function showBlockDays() {
	var type_cur = $("#repeat_select option:selected").val();
	var type_last = $("#repeat_select option:last").val();
	var type_first = $("#repeat_select option:first").val();
	var period = $("#bl_repeat_period");
	var days = $("#bl_repeat_list_days");
	if (type_cur == type_first) {
		days.slideUp("fast");
		period.slideUp("fast");	
		removeRulesBlockRepeatListDays();
		removeRulesBlockRepeatDateStart();
		removeRulesBlockRepeatDateStop();
	} else {
		if (type_cur == type_last) {
			initBlockRepeatDays();
			days.slideDown("fast");		
		} else {
			days.slideUp("fast");
		}
		period.slideDown("fast");
		removeRulesBlockRepeatListDays();
		addRulesBlockRepeatDateStart();	
		if ($("input[name=interval]:checked").attr("id") == "repeat_interval_record") addRulesBlockRepeatDateStop()
	}
}
// выделить день повторения
function selectRepeatDays(inp) {
	var block = inp.parent();
	if (inp.attr("checked")) {
		block.addClass("act_day");
		$("#error_days_repeat").html("");
	} else {
		block.removeClass("act_day");
	}
}
// получить день недели
function getDayWeek() {
	var d = new Date();
	var weekday = new Array(7);
	weekday[0] = "day_sun";
	weekday[1] = "day_mon";
	weekday[2] = "day_tue";
	weekday[3] = "day_wed";
	weekday[4] = "day_thu";
	weekday[5] = "day_fri";
	weekday[6] = "day_sat";
	return weekday[d.getDay()];
}
function initBlockRepeatDays() {
	var count = $("#repeat_list_days li input[type=checkbox]:checked").size();
	if (count == 0) {
		var id = getDayWeek();
		$("#" + id).attr("checked", "checked");
		$("#" + id).parent().addClass("act_day");
	}
	$("#error_days_repeat").html("");
}
// получить текущую дату
function getCurrentDate(delim) {
	var date = new Date();
	var day = ((String(date.getDate()).length == '1')) ? "0" + date.getDate() : date.getDate();
	var month = ((String(date.getMonth() + 1).length == '1')) ? "0" + (date.getMonth() + 1) : (date.getMonth() + 1);
	var year = date.getFullYear();
	return day + delim + month + delim + year;
}
// установить текущую дату
function setCurrentDate(start_date, stop_date) {
    if (!start_date) start_date = getCurrentDate(".");
    if (!stop_date) stop_date = getCurrentDate(".");
	$("#start_date").val(start_date);
	$("#stop_date").val(stop_date);
	$("#repeat_start_date").val(start_date);
	$("#repeat_stop_date").val(stop_date);
}
// установить продолжительность
function setDuration(duration) {
    if (duration){
        duration =  parseFloat(duration.replace(",", "."));
        if (duration - Math.floor(duration)>0){
            $("#duration").val(duration.toFixed(2));
        }else{
            $("#duration").val(duration);
        }
    }else calculateDuration();	
}
// получить текущее время
function getCurrentHour() {
	var cdate = new Date();
	var chour = cdate.getHours()
	var cminute = cdate.getMinutes();
	return chour;
}
// установить текущее время
function setCurrentTime(start_time, stop_time) {
    var chour = getCurrentHour();
    if (!start_time) start_time = chour + ":00"
	if (!stop_time){	    
	    if (chour < 23) stop_time = chour + 1 + ":00"
	    else stop_time = "00:00"
	}
	$("#repeat_start_time").val(start_time);
	$("#time_start").val(start_time);	
	$("#repeat_stop_time").val(stop_time);
	$("#time_stop").val(stop_time);
}
// целый день
function checkAllDay(inp) {
	var start = $("#bl_time_start input");
	var cur_start = $("#current_time_start");
	var stop = $("#bl_time_stop input");
	var cur_stop = $("#current_time_stop");
	if (inp.attr("checked")) {
		start.addClass("inp_txt_dis");
		start.attr("disabled", "disabled");
		cur_start.val(start.val());
		start.val("00:00");		
		stop.addClass("inp_txt_dis");
		stop.attr("disabled", "disabled");
		cur_stop.val(stop.val());
		stop.val("00:00");	
		checkErrorTimeExist();
	} else {
		start.removeClass("inp_txt_dis");
		start.attr("disabled", false);
		start.val(cur_start.val());
		stop.removeClass("inp_txt_dis");
		stop.attr("disabled", false);
		stop.val(cur_stop.val());
	}
}
// функции для расширенных параметров
function funcsAdvancedParams() {
	$("#link_more_set").click(function() {
		showAdvancedParams($(this));
		return false;
	});
	initFuncsResolution();
	$("#video_time").change(function() {
		checkVideoTime();
	});
	$("#video_fps").attr("maxlength", "2");
	$("#video_fps_main").attr("maxlength", "2");
	$("#video_time_hour").attr("maxlength", "2");
	$("#video_time_min").attr("maxlength", "2");
	$("#video_time_sec").attr("maxlength", "2");
}
// инициализация функции для разрешения
function initFuncsResolution() {
	$("#video_resolution").change(function() {
		checkVideoResolution();
		setResolution();
	});
	$("#video_width").change(function() {
	    checkVideoWidth(parseInt($(this).val()));
		setResolution();
	});
	$("#video_height").change(function() {
	    checkVideoHeight(parseInt($(this).val()));
		setResolution();
	});
	initVideoWidthHeight();
}
// инициализация функции для разрешения - другое
function initVideoWidthHeight(){
    var width = $("#video_width").val();
    var height = $("#video_height").val();
    if (!width || !height){
        var type = $("#video_resolution option:selected").text();
        if (type == -1) type = $("#video_resolution option:first").text();
        var arr = type.split("*");        
        $("#video_width").val(parseInt(arr[0], 10));
        $("#video_height").val(parseInt(arr[1], 10));
    }
}
// проверка разрешения
function checkVideoResolution() {
	var type = $("#video_resolution option:selected").val();
	var block = $("#bl_video_resolution_other");
	var error_block = $("#error_video_resolution");
	if (type == "-1") {
		block.slideDown("fast");		
		addRulesVideoWH();        
	} else {
		block.slideUp("fast");
		removeRulesVideoWH();
		error_block.html("");
		$("#bl_video_resolution_other input[type=text]").removeClass("err_forms");
	}
}
// проверка продолжительности
function checkVideoTime() {
	var type = $("#video_time option:selected").val();
	var block = $("#bl_video_time_other");
	if (type == "0") {
		block.slideDown("fast");
		//addRulesVideoTime();
	} else {
		block.slideUp("fast");
		//removeRulesVideoTime();
	}	
}
function setDelimiter(id){
    if (id == 0){   
		addRulesVideoOtherDuration();
        var time = [];
        time.hour = $("#video_time_hour").val();
        time.minute = $("#video_time_min").val();
        time.second = $("#video_time_sec").val();
        $("#value_time_video").val(parseInt(time.hour, 10)*60*60 + parseInt(time.minute, 10)*60 + parseInt(time.second, 10));
    } else {
		removeRulesVideoOtherDuration();
		$("#error_video_duration").html("");
		$("#bl_video_time_other input[type=text]").removeClass("err_forms");
        var period = $("#video_time option:selected").val();
        $("#value_time_video").val(period);	
    }
}
// Подсчет продолжительности
function calculateDuration(){
        var st_time = $("#repeat_start_time").val().split(":");
        var sp_time = $("#repeat_stop_time").val().split(":");
        var start_time = parseInt(st_time[0], 10)*60+parseInt(st_time[1], 10);
        var stop_time = parseInt(sp_time[0], 10)*60+parseInt(sp_time[1], 10);

        if (start_time>=0 && stop_time>=0){
            var duration_type = $("#duration_type").val();
            
            var duration = $("#duration").val();
            if (duration_type == "0") duration = duration*1;
            else if (duration_type == "1") duration = duration*60;
            else if (duration_type == "2") duration = duration*60*24;
            day = parseInt(duration/60/24);

            if (stop_time >= start_time) new_duration = (stop_time-start_time);
            else new_duration = 24*60-(start_time-stop_time);

            duration = (day*24)*60+new_duration;
            /*
            if (duration_type == 2){ // days
                duration = day+new_duration/60/24;
            }else if (duration_type != 0){ //  hours
                duration = day*24+new_duration/60;            
            }else{duration = (day*24)*60+new_duration;}
            */
            if (duration < 60){
                duration_type = 0;
            }else if (duration < 60*60){
                duration_type = 1;
                duration = duration/60;
            }else{
                duration_type = 2;
                duration = duration/60/24;
            }
            
            if (duration - Math.floor(duration)>0){
                $("#duration").val(duration.toFixed(2));
            }else{
                $("#duration").val(duration);
            }
            $("#duration_type").val(duration_type);
        }
}
function calcDuration(duration_type){
    var val = $("#last_duration").val();
    $("#last_duration").val(duration_type);

    duration = $("#duration").val();
    if (val == "0") duration = duration*1;
    else if (val == "1") duration = duration*60;
    else if (val == "2") duration = duration*60*24;
                
    if (duration_type == "0") duration = parseInt(duration);
    else if (duration_type == "1") duration = duration/60;
    else if (duration_type == "2") duration = duration/60/24;
    
    if (duration - Math.floor(duration)>0){
        $("#duration").val(duration.toFixed(2));
    }else{
        $("#duration").val(duration);
    }    
    calculateStopDate();
}
// Подсчет времени при изменении продолжительности
function calculateStopDate(){
    var duration = parseFloat($("#duration").val(), 10).toFixed(2);
    if (duration && parseInt(duration, 10)>=0){
        var st_time = $("#repeat_start_time").val().split(":");
        var start_time = parseInt(st_time[0], 10)*60+parseInt(st_time[1], 10);

        var duration_type = $("#duration_type").val();        
        if (duration_type == 0){ // min
            stop_time = start_time+duration*1;          
        }else if (duration_type == 2){ // days
            stop_time = start_time+duration*60*24;
        }else{ //  hours
            stop_time = start_time+duration*60;            
        }
        var d = 24*60;
        while (stop_time>d) stop_time -= d;
        var dhour = Math.floor(stop_time / 60);
        var dmin = Math.floor(stop_time % 60);
        $("#repeat_stop_time").val((dhour>=10?(dhour>23?"00":dhour):"0"+dhour)+":"+(dmin>=10?dmin:"0"+dmin));
    }
}
// Смена типа сигнала на постоянную запись 
function setSimpleSignal(){
    $("input[name=signal]:checked").attr("checked", false);
    $("#signal_simple").attr("checked", "checked");   
}
// Установка разрешения
function setResolution(){
    var resol = $('#video_resolution option:selected');
    resol_val = resol.val();
    if (resol_val>0) $("#resolution").val(resol.text());
    else if (resol_val == 0) $("#resolution").val($("#camera_resolution").val());
    else $("#resolution").val($("#video_width").val()+"*"+$("#video_height").val());
}
// Проверка корректности продолжительности записи
function checkDuration(){
    var dur = $("#duration").val();
    var d = 24*60;

    while (dur>d) dur -= d;
    
    var st_time = $("#repeat_start_time").val().split(":");
    var sp_time = $("#repeat_stop_time").val().split(":");
    var start_time = parseInt(st_time[0], 10)*60+parseInt(st_time[1], 10);
    var stop_time = parseInt(sp_time[0], 10)*60+parseInt(sp_time[1], 10);
    
    if (start_time && stop_time){
        if (stop_time > start_time) duration = (stop_time-start_time);
        else duration = 24*60-(start_time-stop_time);
    
        if (dur != duration){
            var duration_type = $("#duration_type").val();
            if (duration_type == 2){ // days
                duration = duration/60/24;
            }else if (duration_type != 0){ //  hours
                duration = duration/60;
            }
            if (duration - Math.floor(duration)>0){
                $("#duration").val(duration.toFixed(2));
            }else{
                $("#duration").val(parseInt(duration, 10));
            }
        }
    }
}
function checkVideoWidth(val){
    if (val % 2 > 0) $("#video_width").val(val+1);
}
function checkVideoHeight(val){
    if (val % 2 > 0) $("#video_height").val(val+1);
}
// получить строку даты
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
// проверка валидности периода дат
function checkDateRangeValidator(id_start, id_stop) {
	var objStart = $("#" + id_start).val().split(".");
	var objStop = $("#" + id_stop).val().split(".");
	var strStart = get_DateString(objStart);
	var strStop = get_DateString(objStop);
	var intStart = Date.parse(strStart);
	var intStop = Date.parse(strStop);
	return [intStart, intStop];
}
// инициализация правил для формы
function initRulesForm() {
	if ($("input[name=signal_type]:checked").attr("id") == "record_detectors") addRulesDetectors()
	if ($("input[name=repeat_task]:checked").attr("id") == "repeat_task_yes") 
		addRulesBlockRepeat()
	else 
		addRulesBlockNoRepeat()
	showBlockDays();
	checkVideoOtherDuration();
	checkVideoResolution();
}
function goBack(){
    location.href = "/archive/page_tasks/";
}
// проверка другой продолжительности видеоролика
function checkVideoOtherDuration() {
	var check = $("#video_time option:selected").attr("value");
	if (check == 0) {
		addRulesVideoOtherDuration();
	} else {
		removeRulesVideoOtherDuration();
	}
}