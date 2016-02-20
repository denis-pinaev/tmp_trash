var paramsCarousel = new Array();
var count_prim = 10;
// filters
function initFilters() {
	$("#link_more_search").click(function() {
		var block = $("#block_more_search");
		if (block.css("display") == "none") {
			block.slideDown("normal");
			$(this).html(TEXT_MORE_SEARCH_HIDE);
			var checks = $("#block_more_search input[type=checkbox].check_filter");
			$.each(checks, function() {
				blockFilter($(this));
			});
		} else {
			block.slideUp("normal");
			$(this).html(TEXT_MORE_SEARCH);
		}
		return false;
	});
	var block = $("#block_more_search");
	if (block.css("display") == "none") {
		$("#link_more_search").html(TEXT_MORE_SEARCH);
	} else {
		var checks = $("#block_more_search input[type=checkbox].check_filter");
		$.each(checks, function() {
			blockFilter($(this));
		});
		$("#link_more_search").html(TEXT_MORE_SEARCH_HIDE);
	}
	$("#block_more_search input[type=checkbox].check_filter").click(function() {
		blockFilter($(this));
	});
	isActiveSpinboxTime();
	$("#list_cameras li input[type=checkbox]").click(function() {
		chooseCamera($(this));
	});
	$("#list_cameras li").mouseover(function() {
		if ($(this).attr("class").indexOf("lc_dis") < 0) {
			showInfoCamera($(this));
		}
	});
	$("#list_cameras li").mouseout(function() {
		$(this).removeClass("lc_over");
		if ($(this).attr("class").indexOf("lc_dis") < 0) {
			closeChangeWindow("easyTooltip_camera");  
		}
	});	
}
// блок для одного фильтра
function blockFilter(inp) {
	var block = inp.parent();
	var enter_inp = block.find("input[type=text]");
	if (inp.attr("checked")) {
		block.removeClass("filter_param_dis");
		enter_inp.attr("disabled", false);
		enter_inp.removeClass("err_forms");
		block.find("select").attr("disabled", false);
		if (inp.attr("id") == "filter_defined") {
			$("#filter_defined_param input[type=radio]").attr("disabled", false);
		}
		if (inp.attr("id") == "filter_time") {
			setSpinboxState("filter_time_param", "active");
			addRulesTime();
		}
		if (inp.attr("id") == "filter_id_record") { 
			addRulesIdRecord(); 
		}
		if (inp.attr("id") == "filter_id_person") {
			addRulesIdPerson();
		}	
		if (inp.attr("id") == "filter_cameras") {
			propertiesListCameras("add");
		}
	} else {
		block.addClass("filter_param_dis");
		enter_inp.attr("disabled", "disabled");
		block.find("select").attr("disabled", "disabled");
		if (inp.attr("id") == "filter_defined") {
			$("#filter_defined_param input[type=radio]").attr("disabled", "disabled");
		}		
		if (inp.attr("id") == "filter_time") {
			setSpinboxState("filter_time_param", "disabled");
			removeRulesTime();
			$("#error_ext_search").html("");
		}
		if (inp.attr("id") == "filter_id_record") {
			removeRulesIdRecord();
			$("#error_ext_search").html("");
		}
		if (inp.attr("id") == "filter_id_person") {
			removeRulesIdPerson();
			$("#error_ext_search").html("");
		}		
		if (inp.attr("id") == "filter_cameras") {
			propertiesListCameras("remove");
		}
	}
}
// список камер, добавление/удаление стилей и свойств
function propertiesListCameras(state) {
	var checks = $("#list_cameras li input[type=checkbox]");
	var checks_sel = $("#list_cameras li input[type=checkbox]:checked");
	if (state == "add") {
		checks.attr("disabled", false);
		if (checks_sel.size() > 0) {
			$.each(checks_sel, function() {
				$(this).parent().addClass("lc_act");
			});
		}	
	} else {
		checks.attr("disabled", "disabled");
		if (checks_sel.size() > 0) {
			$.each(checks_sel, function() {
				$(this).parent().removeClass("lc_act");
			});
		}		
	}
}
function initRulesForm() {
	if ($("#filter_time").attr("checked")) addRulesTime();
	if ($("#filter_id_record").attr("checked")) addRulesIdRecord();
	if ($("#filter_id_person").attr("checked")) addRulesIdPerson();
}
// проверка для времени нужно ли делать спинбоксы активными или нет
function isActiveSpinboxTime() {
	var filter = $("#filter_time");
	if (filter.size() > 0) {
		if (filter.attr("checked")) {	
			setSpinboxState("filter_time_param", "active");
		} else {
			setSpinboxState("filter_time_param", "disabled");	
		}
	}
}
// установить состояние спинбоксов в зависимости от активности
function setSpinboxState(id_block, state) {
	var btns = $("#" + id_block + " div.spinbtns input[type=button]");
	if (state == "active") {
		$.each(btns, function() {
			$(this).removeClass("dis");
			$(this).attr("disabled", false);
		});		
	} else {
		$.each(btns, function() {
			$(this).addClass("dis");
			$(this).attr("disabled", "disabled");
		});	
	}
}
/* /filters */
function mainFormFilters() {   
	var filter = $("#filter_time");
	if (!filter.attr("checked")) {
		$("#hour_beg").attr("name", "");
		$("#min_beg").attr("name", "");
		$("#sec_beg").attr("name", "");
		$("#hour_end").attr("name", "");
		$("#min_end").attr("name", "");
		$("#sec_end").attr("name", "");
	}
	filter = $("#filter_defined");
	if (!filter.attr("checked")) {
		$("#ident_yes").attr("name", "");
		$("#ident_no").attr("name", "");
	}
	filter = $("#filter_id_record");
	if (!filter.attr("checked")) {
		$("#id_record").attr("name", "");
	}
	filter = $("#filter_id_person");
	if (!filter.attr("checked")) {
		$("#id_person").attr("name", "");
	}
	filter = $("#filter_fio");
	if (!filter.attr("checked")) {
		$("#person_fio").attr("name", "");
	}
	filter = $("#filter_cameras");
	if (!filter.attr("checked")) {
		$("#cameras").attr("name", "");
	} else {
		addIDCamerasToInput();
	}
	filter = $("#filter_colspans");
	if (!filter.attr("checked")) {
		$("#filter").attr("name", "");
	}
	document.getElementById("mainForm").submit(); 
}
// доюавить id выбранных камер в скрытый инпут
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
// выбрать камеру
function chooseCamera(inp) {
    if (inp.attr("checked")) {
        inp.parent().addClass("lc_act");
    } else {
        inp.parent().removeClass("lc_act");
    }
}
// показать видео с камеры
function showInfoCamera(obj) {
    obj.addClass("lc_over");
    var info = obj.find("input[type=checkbox]").val();
    if (info) {
        var arr = info.split('|');
        var info = $("#easyTooltip_camera div.info_camera");
        var block_img = $("#camera_frame");
        $("#camera_frame").empty();
        info.hide();
        createTitleWindow({id: "easyTooltip_camera", obj: obj.find("label"), width: 200, height: 200, distY: -15 });
        if ( arr.length > 2 ){
	    block_img.find("img").remove();
	    window.stop();
            block_img.html("<img alt='' width='200' src='' id='img_" + (new Date()).getTime() + "' />");
            var img = block_img.find("img");
            img.attr("src", 'http://' + arr[3] + ':' + arr[4] + '/video?uuid=' + arr[2]+'&width=640&height=480&fps={{ fps_of_the_cameras }}');
			$("#camera_name").html(arr[1]);
            info.show(); 
        } else {
            block_img.html("<img alt='' width='200' src='/files/images/camera_200x150.jpg' id='img_" + (new Date()).getTime() + "' />");
            info.show();             
        }      
    }                              
}
// окно для камеры
function createTitleWindow(param) {
    var distX = param.distX ? param.distX : 0; 
    var distY = param.distY ? param.distY : 0; 
    var win = $("#" + param.id);   
    var pos_win = positionScreen({obj: param.obj, win_width: parseInt(win.css("max-width")), win_height: parseInt(win.css("max-height")), distX: distX, distY: distY});
    var coord_left = pos_win.left + "px";
    var coord_top = pos_win.top + "px";
    win.css("left", coord_left);
    win.css("top", coord_top);
    win.show();
}
// инициализация всплыв. подсказки для кнопки Автообновление
function initTooltipAutorefreshLog() {
    $("#btnAuto").easyTooltip({
        useElement: "easyTooltip_auto"
    });        
}
// автообновление журнала
function autorefreshLog(obj) {
	var btn = $(obj);
	var block = $("#easyTooltip_auto");
	if (btn.attr("class").indexOf("off") < 0) {
		btn.addClass("off");
		block.html(AUTO_OFF);
		setCookie('refresh_journal', 'False');
	} else {
		btn.removeClass("off");
		block.html(AUTO_ON);
		setCookie('refresh_journal', 'True');
		doTimeRefresh();
	}
	initTooltipAutorefreshLog();
}
// проверка включено ли автоообновление
function checkAutorefreshLog() {
    var btn = $("#btnAuto");
    var block = $("#easyTooltip_auto");
    var w3 = readCookie('refresh_journal');
    if (w3 == null || w3 == 'True') {
        btn.removeClass("off");
        block.html(AUTO_ON);
    } else {
        btn.addClass("off");
        block.html(AUTO_OFF);    
    }
}
function getArrayChecks() {
	var checks = $("#dataJournal table.table input[type=checkbox]:checked");
	var res = '';
	$.each(checks, function(key, value) {
		if (key != 0) res = res+',';
		res = res + $(this).val();
	});
	return res;
}
// всплывающее информационное окно при клике на лупу
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
// создание карусели идентификаций
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
// инициализация карусели
function initCarousel() {
    $('#carousel').jcarousel();
	clearActiveElemCarusel();	
    $('#carousel li:first').addClass("activeElem");
    /*clearActiveElemCarusel();	
    $("#carousel li a").click(function() {
		alert("test");
        clearActiveElemCarusel();
        $(this).parent().addClass("activeElem");
        return false;
    }); */
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
// при клике на картинку в каруселе
function changePhotos(id) {
    $("#photo_canvas").hide();
    $("#photo_loader").show();
    $.ajax({
    type: "GET",
    url: "/showjournalphoto/"+id,
    data: {small: 'true'},
        success: function(msg) {
			$("#showjournalphoto_photo").html(msg);
            setCheckboxAndDraw();
        }
    });
    return false;
}
// выделение всех строк
function selectedAllRow(id) {
	var inp = $("#" + id);
	var checks = $("#list_records input[type=checkbox].inp_check");
	var checks_all = $("input[type=checkbox].check_all");
	if (inp.attr("checked")) {
		$.each(checks, function() {
			$(this).attr("checked", "checked");
			$(this).parent().parent().addClass("sel");
		});
		checks_all.attr("checked", "checked");
	} else {
		$.each(checks, function() {
			$(this).attr("checked", false);
			$(this).parent().parent().removeClass("sel");
		});
		checks_all.attr("checked", false);	
	}
}
// выделение одной строки
function selectedRow(obj) {
	var inp = $(obj);
	var checks_all = $("input[type=checkbox].check_all");
	var count = $("#list_records input[type=checkbox].inp_check").size();
	var count_sel = 0;
	if (inp.attr("checked")) {
		inp.parent().parent().addClass("sel");
		count_sel = $("#list_records input[type=checkbox].inp_check:checked").size();
		if (count_sel == count) {
			checks_all.attr("checked", "checked");
		}
	} else {	
		inp.parent().parent().removeClass("sel");
		checks_all.attr("checked", false);
	}
}
// фото с камеры, функция на клик изображения с карусели
function changePhoto_(id, obj) {
    clearActiveElemCarusel();	
	$(obj).parent().addClass("activeElem");
    $("#photo_canvas").hide();
    $("#photo_loader").show();
    $.ajax({
    type: "GET",
    url: "/showjournalphoto/"+id,
    data: {small: 'true'},
        success: function(msg) {
			$('#showjournalphoto_photo').html(msg);
			setCheckboxAndDraw();
			initTooltip();
        }
    });
    return false;
}