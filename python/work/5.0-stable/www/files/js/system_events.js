function init() {
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
	initTooltip();
	isActiveSpinboxTime();
}
function blockFilter(inp) {
	var block = inp.parent();
	var enter_inp = block.find("input[type=text]");
	if (inp.attr("checked")) {
		block.removeClass("filter_param_dis");
		enter_inp.attr("disabled", false);
		enter_inp.removeClass("err_forms");
		block.find("select").attr("disabled", false);
		if (inp.attr("id") == "filter_time") {
			setSpinboxState("filter_time_param", "active");
			addRulesTime();
		}
		if (inp.attr("id") == "filter_id") addRulesIdRecord();
		if (inp.attr("id") == "filter_cameras") {
			propertiesListCameras("add");
		}
	} else {
		block.addClass("filter_param_dis");
		enter_inp.attr("disabled", "disabled");
		block.find("select").attr("disabled", "disabled");
		if (inp.attr("id") == "filter_time") {
			setSpinboxState("filter_time_param", "disabled");
			removeRulesTime();
			$("#error_ext_search").html("");
		}
		if (inp.attr("id") == "filter_id") {
			removeRulesIdRecord();
			$("#error_ext_search").html("");
		}
		if (inp.attr("id") == "filter_cameras") {
			propertiesListCameras("remove");
		}
	}
}
function initRulesForm() {
	if ($("#filter_time").attr("checked")) addRulesTime();
	if ($("#filter_id").attr("checked")) addRulesIdRecord();
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