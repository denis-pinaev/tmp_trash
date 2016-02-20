var paramsCarousel = new Array();
var count_prim = 10;
$(function() {
    init();
});
// инициализация
function init() {
    initTooltip();
    initTooltipAuto();
    checkAutoJournal();
    initFuns();
    initFuncsFilter();
    setFreeSpaceDisk();
	checkForm();
	initRulesForm();
}
// всплывающие подсказки
function initTooltip() {
    $(".short_descr").easyTooltip();        
}
function initTooltipAuto() {
    $("a.inp_btnAuto").easyTooltip({
        useElement: "easyTooltip_auto"
    });        
}
// инициализация функций
function initFuns() {
    $("a.inp_btnAuto").click(function() {
        var btn = $(this);
        var block = $("#easyTooltip_auto");
        if (btn.attr("class").indexOf("offAuto") == -1) {
            btn.addClass("offAuto");
             block.html(AUTO_OFF);
             setCookie('refresh_journal', 'False');
        } else {
            btn.removeClass("offAuto");
            block.html(AUTO_ON);
            setCookie('refresh_journal', 'True');
        }
        initTooltipAuto();
        return false;
    });  
}

function checkAutoJournal() {
    var btn = $("a.inp_btnAuto");
    var block = $("#easyTooltip_auto");
    var w3 = readCookie('refresh_journal');
    if (w3==null || w3 == 'True') {
        btn.removeClass("offAuto");
        block.html(AUTO_ON);
    } else {
        btn.addClass("offAuto");
        block.html(AUTO_OFF);    
    }
}
// инициализация карусели
function initCarousel() {
    $('#carousel').jcarousel();
    clearActiveElemCarusel();
    $('#carousel li:first').addClass("activeElem");
    $("#carousel li a").click(function() {
        clearActiveElemCarusel();
        $(this).parent().addClass("activeElem");
        return false;
    }); 
    $('#carousel').jcarousel({
        itemLoadCallback: itemLoadCallbackFunction
    });   
}
function itemLoadCallbackFunction(carousel, state) {
    var count_elem = paramsCarousel.length - 1;
    var count_curr = $("#carousel li").size();
    if ((count_elem > count_prim) || (count_elem < count_curr)) {
        if (state == "next") {
            for (var i = (carousel.last + 1); i <= (carousel.last + 3); i++) {
                if ((typeof(paramsCarousel[i])) != 'undefined') {
                    carousel.add(i, paramsCarousel[i]);
                }  
            }
            size = $("#carousel li").size();
            carousel.size(size); 
            return;
        }
    }                                                 
}
function clearActiveElemCarusel() {
    var blocks = $("#carousel li");
    $.each(blocks, function() {
        $(this).removeClass("activeElem");
    })
}
// обучение как шум
function personsForNoise(count, name_block) {
    var txt;
    var head;
    var check = isChecked(count);
    persIdVals = new Array();
    var ident = false;
    var a = 0;
    for (i=1; i<=count;i++)
    {
        if($('#check' + i).is(':checked')) {
            if($('#img_id_' + i).attr('ident') == 1){
                ident = true;
            }
            persIdVals[a] = $('#check' + i).val();
            a++;
        }
    }
    if(ident || persIdVals.length == 0){
        txt = createTextMessage({name_block: "win_persontraining_wrong", count: 0 });
        changeWindow({id: 'win_persontraining_wrong', css: {width: '300px', height: '200px'}, txt: txt});
    } else {
        changeWindow2({id: 'win_learn', txt: replace_string(LEARN_AS_NOISE, '{}', '(' + check + ')')});
        //showPersonTrainingDialog('group');
    }
}
function onClickLearningNoise(){
    var url = '/noiselist_result/?journal_ids=' + persIdVals.join(',');
    document.location = url;
}
function showJournalPhoto(id, num){
    showIndicator(true);
    $.ajax({
        type: "GET",
        url: "/showjournalphoto/"+id,
        data: {},
        success: function(msg) {
            showIndicator(false);       
            $("#win_journalphoto_contWF").html(msg);
            createCarousel();
            changeWindow2({id: 'win_journalphoto', css: { "width": "525px", "height": "550px" }});
            initCarousel();
            initTooltip();
        },
        error: function() {
            showIndicator(false);
        }
    });
}
function createCarousel() {
    var count_elem = paramsCarousel.length - 1;
    $("#win_journalphoto_carousel").html('<ul id="carousel" class="jcarousel-skin-tango"></ul>');
    var cont_prim = "";
    if (count_elem > count_prim) {      
        for (var i = 1; i <= count_prim; i++) {
            cont_prim += paramsCarousel[i];
        }
    } else {
        for (var i = 1; i <= count_elem; i++) {
            cont_prim += paramsCarousel[i];
        }                 
    }
    $("#carousel").html(cont_prim); 
}
function changePhoto_(id) {
    $("#photo_canvas").hide();
    $("#photo_loader").show();
    $.ajax({
    type: "GET",
    url: "/showjournalphoto/"+id,
    data: {small: 'true'},
        success: function(msg) {
                byId('showjournalphoto_photo').innerHTML = msg;
                setCheckboxAndDraw();
        }
    });
    return false;
}
function closeDatePicker() {
    var datepicker = $("#datepicker");
    if (datepicker.size() > 0) datepicker.hide()
}
// инициализация функций для фильтра
function initFuncsFilter() { 
	if ($("#block_all_filter").size() > 0) {
		$("#filter_journal").change(function() {
			showBlockFilter();
		});
		$(".check_filter").click(function() {
			hideBlockFilter($(this));
		});    
		$("#list_cameras li input[type=checkbox]").click(function() {
			chooseCamera($(this));
		});
		$("#list_cameras li").mouseover(function() {
			showInfoCamera($(this));
		});
		$("#list_cameras li").mouseout(function() {
			closeChangeWindow("easyTooltip_camera");    
		});
	}
}
function showInfoCamera(obj) {
    var info = obj.find("input[type=checkbox]").val();
    if (info) {
        var arr = info.split('|');
        var indicator = $("#easyTooltip_camera div.indicator_camera");
        var info = $("#easyTooltip_camera div.info_camera");
        var block_img = $("#camera_frame");
        $("#camera_frame").empty();
        info.hide();
        indicator.show();
        createTitleWindow({id: "easyTooltip_camera", obj: obj.find("label"), width: 200, height: 200, distY: -15 });
        if ( arr.length > 3 ){
            var d = new Date();
            $.ajax({
                type: "GET",
                url: "/get-ident-video-frame/",
                data: {'host': arr[3], 'port': arr[4], 'numcamera': arr[5], 'rnd': d.getTime()},
                success: function(data) {
                    block_img.html("<img alt='' width='200' src='' id='img_" + (new Date()).getTime() + "' />");
                    var img = block_img.find("img");
                    if (data.res != 'success') {
                        img.attr("src", '/files/images/camera_200x150.jpg')
                    } else {
                        if (data.error_remark == "frame isn't got" || data.image.length == 0){
                            img.attr("src", '/files/images/camera_200x150.jpg');
                        }else{
                            var buffer = "data:image/jpeg;base64," + data.image;
                            img.attr("src", buffer);
                        }
                    }
                    delete data;
                    $("#camera_name").html(arr[1] + ":" + arr[2]);
                    indicator.hide();  
                    info.show();
                },
                error: function(data) {  
                    block_img.html("<img alt='' width='200' src='/files/images/camera_200x150.jpg' id='img_" + (new Date()).getTime() + "' />");
                    indicator.hide();  
                    info.show();                     
                }
            });     
        } else {
            block_img.html("<img alt='' width='200' src='/files/images/camera_200x150.jpg' id='img_" + (new Date()).getTime() + "' />");
            indicator.hide();  
            info.show();             
        }      
    }                              
}
// показать фильтр
function showBlockFilter() {
    var num_filter = $("#filter_journal option:selected").attr("value");
    if (num_filter == 1) {
        showBlockFilterParam("block_filter_time", "filter_time");    
    } else if (num_filter == 2) {
        showBlockFilterParam("block_filter_ident", "filter_ident");
    } else if (num_filter == 3) {
        showBlockFilterParam("block_filter_cameras", "filter_cameras");              
    } else if (num_filter == 4) {
        showBlockFilterParam("block_filter_fio", "filter_fio");
    } else if (num_filter == 5) {
        showBlockFilterParam("block_filter_id_person", "filter_id_person");                    
    } else if (num_filter == 6) {
        showBlockFilterParam("block_filter_id_record", "filter_id_record"); 
    } else if (num_filter == 7) {
        showBlockFilterParam("block_filter_colspans", "filter_colspans");    
    }
    $("#filter_journal option:selected").attr("disabled", "disabled");
    $("#filter_journal option[value=0]").attr("selected", "selected");
}
function showBlockFilterParam(id_block, id_filter) {
    var block = $("#" + id_block);
    if (block.css("display") == "none") {
        $("#" + id_filter).attr("checked", "checked");
        block.slideDown("normal");
        if (id_block == "block_filter_cameras") {
            checkBlockFilterCameras();
		} else if (id_block == "block_filter_fio") {
            $("#person_fio").focus();
			$("#person_fio").removeClass("err_forms");
			$("#bl_error_person_fio").html("");
			addRulesFIOPerson();
        } else if (id_block == "block_filter_id_record") {
            $("#id_record").focus();
			$("#id_record").removeClass("err_forms");
			$("#id_record").parent().parent().prev().html("");
			addRulesIdRecord();
        } else if (id_block == "block_filter_id_person") {
            $("#id_person").focus();
			$("#id_person").removeClass("err_forms");
			$("#id_person").parent().parent().prev().html("");			
			addRulesIdPerson();
        } else if (id_block == "block_filter_colspans") {
            $("#filter").focus();
        }
    }
}
// проверка есть ли в блоке выделенные камеры
function checkBlockFilterCameras() {
    var checks = $("#list_cameras li input[type=checkbox]:checked");
    if (checks.size() > 0) {
        $.each(checks, function() {
            $(this).parent().addClass("lc_check");
        })
    }                                    
}
// скрыть фильтр
function hideBlockFilter(inp) {	
	var id_block = "block_" + inp.attr("id");
	$("#" + id_block).slideUp("normal");
	if (inp.attr("id") == "filter_id_person") removeRulesIdPerson();
	if (inp.attr("id") == "filter_id_record") removeRulesIdRecord();
	if (inp.attr("id") == "filter_fio") removeRulesFIOPerson();
	var filters = $("#block_all_filters").find("div.block_filter_param");
	var index = 0;
	$.each(filters, function(key, value) {
		if ($(this).attr("id") == id_block) {
			index = key;
		}
	});
	$("#filter_journal option").eq(index).attr("disabled", false);	
}
// выбрать все камеры
function chooseAllCameras(inp) {
    var checks = $("#list_cameras input[type=checkbox]");
    if (inp.attr("checked")) {
        $.each(checks, function() {
            $(this).attr("checked", "checked");
            $(this).parent().addClass("lc_check");
        });
    } else {
        $.each(checks, function() {
            $(this).attr("checked", false);
            $(this).parent().removeClass("lc_check");
        });    
    }
}
// выбрать камеру
function chooseCamera(inp) {
    if (inp.attr("checked")) {
        inp.parent().addClass("lc_check");
    } else {
        inp.parent().removeClass("lc_check");
    }
}
function mainFormFilters() {   
   var block_ident = $("#block_filter_fio");
   var inp_ident = $("#filter_fio");
   if ((block_ident.css("display") != "block") || (!inp_ident.attr("checked"))) {
        $("#person_fio").attr("name","");
   }
   block_ident = $("#block_filter_cameras");
   inp_ident = $("#filter_cameras");
   if ((block_ident.css("display") == "block") && (inp_ident.attr("checked"))) {
      addIDCamerasToInput();
   }else{
        $("#cameras").attr("name","");
   }  
   block_ident = $("#block_filter_colspans");
   inp_ident = $("#filter_colspans");
   if ((block_ident.css("display") != "block") || (!inp_ident.attr("checked"))) {
        $("#filter").attr("name","");
   } 
   block_ident = $("#block_filter_id_record");
   inp_ident = $("#filter_id_record");
   if ((block_ident.css("display") != "block") || (!inp_ident.attr("checked"))) {
        $("#id_record").attr("name","");
   }
   block_ident = $("#block_filter_id_person");
   inp_ident = $("#filter_id_person");
   if ((block_ident.css("display") != "block") || (!inp_ident.attr("checked"))) {
        $("#id_person").attr("name","");
   }
   block_ident = $("#block_filter_time");
   inp_ident = $("#filter_time");
   if ((block_ident.css("display") != "block") || (!inp_ident.attr("checked"))) {
        $("#time_hour_beg").attr("name","");
        $("#time_min_beg").attr("name","");
        $("#time_hour_end").attr("name","");
        $("#time_min_end").attr("name","");
   }
   document.getElementById("mainForm").submit(); 
}
// сбросить фильтры
function resetFilters() {
	var filters = $("#block_all_filters").find("div.block_filter_param");
	var block;
	$.each(filters, function(key, value) {
		if (key > 0) {
			block = $(this);
			block.find("input[type=checkbox].check_filter").attr("checked", false);
			block.slideUp("normal");
			if (block.attr("id") == "block_filter_cameras") $("#list_cameras li input[type=checkbox].inp_check").attr("checked", false);
			if (block.attr("id") == "block_filter_fio") $("#person_fio").val("");
			if (block.attr("id") == "block_filter_id_record") $("#id_record").val("");
			if (block.attr("id") == "block_filter_id_person") $("#id_person").val("");
			if (block.attr("id") == "block_filter_colspans") $("#filter").val("");
			if (block.attr("id") == "block_filter_time"){
				$("#time_hour_beg").attr("name","");
				$("#time_min_beg").attr("name","");
				$("#time_hour_end").attr("name","");
				$("#time_min_end").attr("name","");
			}
		}
	});
	$("#filter_journal option").attr("disabled", false);
	setCurrentDate(".", "dateBegin", "dateEnd");
	$('#mainForm').submit();
}
function addIDCamerasToInput() {
   var checks = $("#list_cameras li input[type=checkbox]:checked");
   if (checks.size() > 0) {
      var array = [];
      $.each(checks, function(key, value) {
          array[key] = $(this).attr("id").split("_")[1];
      });
      $("#cameras").val("[" + array + "]");
   }
}
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
// установить текущую дату
function setCurrentDate(delim, id_beg, id_end) {
	var date = new Date();
	var day = ((String(date.getDate()).length == '1')) ? "0" + date.getDate() : date.getDate();
	var month = ((String(date.getMonth() + 1).length == '1')) ? "0" + (date.getMonth() + 1) : (date.getMonth() + 1);
	var year = date.getFullYear();
	var date = day + delim + month + delim + year;
	$("#" + id_beg).val(date);
	if ($("#" + id_end).size() > 0) $("#" + id_end).val(date);
}
// проверки на валидность
// проверить дату на корректность
function checkDateValidator(date) {
	var regexp = /^([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})$/;
	if (regexp.test(date)) {
		var arr = regexp.exec(date);
		if (arr[1] < 32 && arr[1] > 0 && arr[2] < 13 && arr[2] >= 0 && arr[3] > 1900) {		    
			var dt = new Date(arr[3], arr[2]-1, arr[1]);		    
			if (dt && dt.getDate()==arr[1] && (dt.getMonth()+1)==arr[2] && dt.getFullYear()==arr[3]) return true;
		}
		return false;
	} 
	return false;
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
function initRulesForm() {
	if ($("#filter_id_person").attr("checked")) addRulesIdPerson();
	if ($("#filter_id_record").attr("checked")) addRulesIdRecord();
	if ($("#filter_fio").attr("checked")) addRulesFIOPerson();
}