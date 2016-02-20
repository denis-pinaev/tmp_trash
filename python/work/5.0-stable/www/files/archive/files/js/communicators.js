function initFuncsCommunicators() {
	initTooltip();
	initFuncs();
	checkFormAddCommunicator();
}
// инициализация всплыв подсказок
function initTooltip() {
    $(".short_descr").easyTooltip();
}
// инициализация функций
function initFuncs() {
    $("#choose_all").click(function() {
        selectAllCommunicators($(this));
    });    
	$("#choose_all2").click(function() {
        selectAllCommunicators($(this));
    });
	$("#list_communicators tr td.td_check input[type=checkbox]").click(function() {
		selectCommunicator($(this));
	});
}
// выделение всех коммуникаторов
function selectAllCommunicators(inp) {
    if (inp.attr("checked")) {
		$("div.bl_btn_check div input[type=checkbox]").attr("checked", "checked");
		$("#list_communicators tr td.td_check input[type=checkbox]").attr("checked", "checked");
		$("div.bl_btn_check2 div input[type=checkbox]").attr("checked", true);
    } else {
		$("div.bl_btn_check div input[type=checkbox]").attr("checked", false);
		$("#list_communicators tr td.td_check input[type=checkbox]").attr("checked", false);
		$("div.bl_btn_check2 div input[type=checkbox]").attr("checked", false);
    }
}
// получить кол-во выделенных строк
function getCountCommunicatorsChoose() {
	return $("#list_communicators tr td.td_check input[type=checkbox]:checked").size();
}
// получить кол-во строк на странице
function getCountCommunicatorsAll() {
	return $("#list_communicators tr td.td_check input[type=checkbox]").size();
}
// выбрать строку
function selectCommunicator(inp) {
    var count_choose = getCountCommunicatorsChoose();
	var count_all = getCountCommunicatorsAll();
	if (count_all == count_choose) $("div.bl_btn_check2 div input[type=checkbox]").attr("checked", "checked");
	else $("div.bl_btn_check2 div input[type=checkbox]").attr("checked", false);
}
// удалить коммуникатор
function deleteCommunicators() {
	var count_choose = getCountCommunicatorsChoose();
	if (count_choose > 0)  {
		changeWindow({id: 'win_del', css: {width: '300px', height: '200px'}, txt: replace_string(MESSAGE[1], '{}', count_choose)});
	} else {
		changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: MESSAGE[0]});
	}
}
// добавить коммуникатор
function addCommunicator() {
	$("#communicator_host").val("");
	$("#communicator_host").removeClass("err_forms");
	$("#communicator_port").val("");
	$("#communicator_port").removeClass("err_forms");
	$("#win_add").find("div.bl_error").html("");
	changeWindow({id: 'win_add', css: {width: '320px', height: '220px'}});
}
// проверка формы добавления коммуникатора
function checkFormAddCommunicator() {
	var validator = $("#frmAddCommunicator").validate({
		rules: {
			host: {
				required: true		
			},
			port: {
				required: true,
				number: true,
				min: 1024,
				max: 65535				
			}
		},
		messages: {
			host: {
				required: ERROR[0]
			},
			port: {
				required: ERROR[1],
				number: ERROR[2],
				min: ERROR[3],
				max: ERROR[3]
			}			
		},
		errorPlacement: function(error, element) {
			error.appendTo( element.parent().parent().prev() ); 
		},
		submitHandler: function() {
			addNewCommunicator();
		}
	});
}
function addNewCommunicator(){
	var options = {
		method: "POST",	  
		url: URL[1],	  
		data: {id: $(":radio[name=index]").filter(":checked").val()},
		success: function(msg) {
			closeChangeWindow('win_add');
			if (msg == "error") showMessage(ERROR[4]);
			else if (msg == "dublicate") showMessage(ERROR[5]);
			else {
				showMessage(MESSAGE[2]);
				$('#communicator_list').html(msg);
			}
		},
		error: function(msg) {
			closeChangeWindow('win_add');
			showMessage(ERROR[4]);
		}
	};
	$("#frmAddCommunicator").ajaxSubmit(options);    
}
function getInputs(name){
	var c = 1;
	var val = "";
	obj = byId(name+c);
	while (obj) {	    
		if (obj.checked) {
			val = val + obj.value + ",";			
		}
		c++;
		obj = byId(name+c);
	}
	return val;
}

function delSelectCommunicators(url){
	closeChangeWindow('win_del');
	showIndicator(true);
	$.ajax({
		type: "POST",
		url: URL[0],
		data: {ids: getInputs("communicator")},
		success: function(msg){
			showIndicator(false);					
			if (msg != "error") {
			    showMessage(MESSAGE[3]);
				$('#communicator_list').html(msg);
			} else{
				showMessage(ERROR[6]);
			}
		},
		error: function(msg) {
		    showIndicator(false);		
		    showMessage(ERROR[6]);  		    
		}
	});    
}
function sort_communicators(id, order){
    byId("id_sort").value = id;
    if (order == 0) byId("id_order").value = 1;
    else byId("id_order").value = 0;
    byId("communicator_form").submit();
}