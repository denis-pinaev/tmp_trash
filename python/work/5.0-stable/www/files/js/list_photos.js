// инициализация функций для выбора лиц
function initSelectFaces() {
    initTooltip();
    initFuncs();
    initValue();
	setupZoom();
}
// инициализация всплыв подсказок
function initTooltip() {
    $(".short_descr").easyTooltip();
    $(".btn_loupe").easyTooltip();
}
// инициализация функций
function initFuncs() {
    $("#menu_cutfaces li a").click(function() {
        if (getCountPhotosChoose() > 0) {
            initMenuFilter($(this));
            checkMenuFilter($(this));
        }
        return false;
    });
    $("#choose_all").click(function() {
        selectAllFaces($(this));
    });
    $("#choose_all2").click(function() {
        selectAllFaces($(this));
    });   
    $("#list_photos li input[type=checkbox]").click(function() {                                                                  
        selectFace($(this));
    });
    $("#list_photos li div.block_photo").click(function() { 
        var inp = $(this).parent().find("input[type=checkbox]");
		if (inp.attr("checked")) inp.attr("checked", false)
		else inp.attr("checked", "checked");		
        selectFace(inp);
    });
}
function initValue() {
    var count =  $("#list_photos li").size();
    if (count > 0) {
        $("#choose_all").attr("checked", "checked");
        $("#choose_all2").attr("checked", "checked");
        $("#list_photos li").addClass("lp_act");
        $("#list_photos li input[type=checkbox]").attr("checked", "checked");
        $("#count_choose").html(count);
        $("#menu_cutfaces li a.link_choose").parent().removeClass("mcf_dis");                    
    }
}
// инициализация меню фильтра
function initMenuFilter(obj) {
    $("#menu_cutfaces li").removeClass("mcf_act");
    obj.parent().addClass("mcf_act");
}
// получить количество выделенных фото
function getCountPhotosChoose() {
    var block_choose = $("#count_choose");
    return parseInt(block_choose.html());
}
// выделение фото
function selectFace(inp) {
    var block_choose = $("#count_choose");
    var count_choose = getCountPhotosChoose();
	var count_all = $("#list_photos li").size();
    var link_choose = $("#menu_cutfaces li a.link_choose");
    if (inp.attr("checked")) {
        count_choose++
        link_choose.parent().removeClass("mcf_dis");
		inp.parent().parent().addClass("lp_act");
    } else {
        count_choose--
		inp.parent().parent().removeClass("lp_act");
        if (count_choose == 0) {
            link_choose.parent().addClass("mcf_dis");
        }
    }
    if (count_choose == 0) count_choose = "0";
	if (count_all == count_choose) $("div.bl_btn_check div input[type=checkbox]").attr("checked", "checked");
	else $("div.bl_btn_check div input[type=checkbox]").attr("checked", false);
    block_choose.html(count_choose);
}
function selectAllFaces(inp) {
    var block_choose = $("#count_choose");
    var count_choose = "0";
    var link_choose = $("#menu_cutfaces li a.link_choose");
    if (inp.attr("checked")) {
		$("div.bl_btn_check div input[type=checkbox]").attr("checked", "checked");
		$("#list_photos li").addClass("lp_act");
		$("#list_photos li input[type=checkbox]").attr("checked", "checked");
        count_choose = $("#list_photos li input[type=checkbox]:checked").size();
        link_choose.parent().removeClass("mcf_dis");
    } else {
		$("div.bl_btn_check div input[type=checkbox]").attr("checked", false);
		$("#list_photos li").removeClass("lp_act");
		$("#list_photos li input[type=checkbox]").attr("checked", false);		
        link_choose.parent().addClass("mcf_dis");	
    }
    block_choose.html(count_choose);
}
// проверка, какое тип выбрали
function checkMenuFilter(obj) {
    var link = obj;
    var block_btn1 = $("#bl_btn_check_up");
    var block_btn2 = $("#bl_btn_check_down");
    var list = $("#list_photos");    
    var list_choose = $("#list_photos_choose");
    if (link.attr("class") && (link.attr("class").indexOf("link_choose") > -1)) {
        block_btn1.css("opacity", "0");
        block_btn2.hide();
        list.hide();
        showOnlySelectFace();
    } else {
        block_btn1.css("opacity", "1");
        block_btn2.show();
        list_choose.hide();
        list.show();    
    }
}
// показать только выделенные лица
function showOnlySelectFace() { 
    var checks = $("#list_photos li input[type=checkbox]:checked");
    var list_choose = $("#list_photos_choose");
    var content = "";
    $.each(checks, function() {
        content = content + "<li>" + $(this).parent().parent().html() + "</li>";
    });
    list_choose.html(content);
    $("#list_photos_choose li div.block_check").css("display", "none");
    list_choose.show();
    setupZoom();
    initTooltip();
}
// инициализация функций для результата обучения
function initResultLearn() {
    initTooltip();
    checkCountElemFilter();
    $("#menu_cutfaces li a").click(function() {
        var li = $(this).parent();
        if ((li.attr("class") && (li.attr("class").indexOf("mcf_dis") == -1) || (!li.attr("class")))) {                              
            initMenuFilter($(this));
            showFilterResult($(this));
        }
        return false;
    });        
}
// проверка сколько элементов в фильтре
function checkCountElemFilter() {
    var count_all = parseInt($("#count_all").html());
    var count_learn = parseInt($("#count_learn").html());
    var count_nolearn = parseInt($("#count_nolearn").html());
    if (count_learn == 0) {
        $("#link_learn").parent().addClass("mcf_dis");
    }
    if (count_nolearn == 0) {
        $("#link_nolearn").parent().addClass("mcf_dis");
    }
}
// показать результаты фильтра
function showFilterResult(obj) {
    var type = obj.attr("id").split("_")[1];
    $(".list_result_learn").hide();
    if (type == "learn") {
        showFilterResultLearn();
    } else if (type == "nolearn") {
        showFilterResultNoLearn();
    } else {
        showFilterResultAll();
    }
}
// показать только обученных
function showFilterResultLearn() {
    $("#count_cur").html($("#count_learn").html());
    var elem = $("#list_all li.lrl_success");
    var list = $("#list_learn");
    var content = "";
    $.each(elem, function() {
        content = content + "<li class='lrl_success'>" + $(this).html() + "</li>";
    });
    list.html(content);
    list.show();
    setupZoom();
    initTooltip();    
}
// показать только необученных
function showFilterResultNoLearn() {
    $("#count_cur").html($("#count_nolearn").html());
    var elem = $("#list_all li.lrl_error");
    var list = $("#list_nolearn");
    var content = "";
    $.each(elem, function() {
        content = content + "<li class='lrl_error'>" + $(this).html() + "</li>";
    });
    list.html(content);
    list.show();
    setupZoom();
    initTooltip();    
}
// показать всё
function showFilterResultAll() {
    $("#count_cur").html($("#count_all").html());
    $("#list_all").show();
    setupZoom();
    initTooltip();    
}