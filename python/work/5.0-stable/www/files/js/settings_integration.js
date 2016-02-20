var params = new Array();
var TIME_SHOW_MESSAGE = 3000; // время показа сообщения
function initTooltip() {
    $(".short_descr").easyTooltip();
}
// инициализация функций для SMTP
function initSMTP() {
    $("input[name=system_control_smtp_need_alert]").click(function() {
        showSettings($(this), 'smtp');
        checkAlertSMTP();
        checkAuthSMTP();
    });
    $("input[name=system_control_smtp_mail_auth]").click(function() {
        settingsSMTPAuth($(this));
    });
    checkAlertSMTP();
    checkFormSettingsSMTP();
    checkAuthSMTP(true);
	initFuncsBtnSave("smtp");
}
// проверка включен или нет SMTP
function checkAlertSMTP() {
    var inp = $("input[name=system_control_smtp_need_alert]:checked");
    if (inp.attr("id") == "smtp_need_alert_yes") {
        $("#settings_smtp").show();
    } else {
        $("#settings_smtp").hide();
    }                           
}
// показать/скрыть настройки
function showSettings(inp, protocol) {
    var id = inp.attr("id");
    var block = $("#settings_" + protocol)
    if (id.indexOf("_no") > -1) {
        block.slideUp("normal");
        if (protocol == "smtp") {
            removeRulesSettingsSMTP();
        } else if (protocol == "snmp") {
            removeRulesSettingsSNMP();
        } else {
			removeRulesSettingsUniversal();
		}
    } else {
        if (protocol == "smtp") {
            addRulesSettingsSMTP();
        } else if (protocol == "snmp") {
            addRulesSettingsSNMP();
        } else {
			addRulesSettingsUniversal();
		}
        block.slideDown("normal");
    }
}
// проверка включена ли авторизация
function checkAuthSMTP(upload) {
    var inp = $("input[name=system_control_smtp_mail_auth]:checked");
    settingsSMTPAuth(inp, upload);
}
// настройка авторизации
function settingsSMTPAuth(inp, upload) {
    var id = inp.attr("id");
    var block_pswd = $("#smtp_password_block");
    if (id == "smtp_mail_auth_no") {
        if (upload) {
            block_pswd.hide();
        } else {
            block_pswd.slideUp("normal");
        }
        removeRulesSettingsSMTPAuth();
    } else {
        if (upload) {
            block_pswd.show();
        } else {
            block_pswd.slideDown("normal");
        }       
        addRulesSettingsSMTPAuth();
    }
}
function addRulesSettingsSMTPAuth() {
    $("#smtp_password").rules("add", {
        required: true,
        messages: {
            required: ERROR4
        }        
    });
    $("#smtp_password").focus();
}
function removeRulesSettingsSMTPAuth() {
    var psw = $("#smtp_password");
    psw.rules("remove");
    psw.removeClass("err_forms");
    psw.parent().parent().prev().html("");
}
// инициализация валидатора
function checkFormSettingsSMTP() {
    var validator = $("#formIntegration").validate({
        errorPlacement: function(error, element) {
            error.appendTo( element.parent().parent().prev() ); 
        },
        submitHandler: function() {
			saveSettings('smtp');
        }        
    });
    var inp = $("input[name=system_control_smtp_need_alert]:checked");
    if (inp.attr("id") == "smtp_need_alert_yes") {
        addRulesSettingsSMTP();
    }
}
// добавление правил для полей
function addRulesSettingsSMTP() {
    $("#smtp_to").rules("add", {
        required: true,
        email: true,
        messages: {
            required: ERROR1,
            email: ERROR2
        }
    });
    $("#smtp_from").rules("add", {
        required: true,
        email: true,
        messages: {
            required: ERROR1,
            email: ERROR3
        }
    });
    $("#smtp_mail_server").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }        
    });
    $("#system_control_smtp_mail_port").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });
    $("#system_control_smtp_identification_alert_timeout").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });
}
// удаление правил для полей
function removeRulesSettingsSMTP() {
    $("#smtp_to").rules("remove");
    $("#smtp_from").rules("remove");
    $("#smtp_mail_server").rules("remove");
    $("#system_control_smtp_mail_port").rules("remove");
    $("#system_control_smtp_identification_alert_timeout").rules("remove");

    $("#formIntegration input[type=text]").removeClass("err_forms");
    $("#formIntegration .bl_error").html("");
}

// инициализация функций для SNMP
function initSNMP() {
    initTooltip();	
    $("input[name=system_control_snmp_need_alert]").click(function() {
        showSettings($(this), 'snmp');
        checkAlertSNMP();
    });
    $("input[name=system_control_snmp_trap_version]").click(function() {
        settingsSNMPVersion($(this));
    });
    $("input[name=system_control_snmp_trap_type]").click(function() {
        settingsSNMPTimeout($(this));
    });
    $("#sortable").sortable();
    $("#snmp_common_upd").keyup(function() {
        if ($(this).val()) { $(this).parent().removeClass("err_forms") }
    })
    checkFormSettingsSNMP();
    checkAlertSNMP();
	initFuncsBtnSave("snmp");
}
// проверка - включён ли протокол SNMP
function checkAlertSNMP() {
    var inp_alert = $("input[name=system_control_snmp_need_alert]:checked");
    var inp_version = $("input[name=system_control_snmp_trap_version]:checked");
    var inp_type = $("input[name=system_control_snmp_trap_type]:checked");
    if (inp_alert.attr("id") == "snmp_need_alert_yes") {
        $("#settings_snmp").show();
        if (inp_version.attr("id") == "snmp_version2") {
            $("#settings_snmp_version2").show();
            initTooltip();
            getIdentOrderSNMP();
            if (inp_type.attr("id") == "snmp_type_inform") {
                $("#settings_snmp_version2_alert_timeout").show();
            } else {
                $("#settings_snmp_version2_alert_timeout").hide();   
            }
        } else {
            $("#settings_snmp_version2").hide();
        }
    } else {
        $("#settings_snmp").hide();
    }                         
}
function settingsSNMPVersion(inp) {
    var id = inp.attr("id");
    var block_set_ver2 = $("#settings_snmp_version2");
    if (id == "snmp_version1") {
        block_set_ver2.slideUp("normal");
        removeRulesSettingsSNMPVersion2()
    } else {
        block_set_ver2.slideDown("normal");
        initTooltip();
        addRulesSettingsSNMPVersion2()
    }
}
function settingsSNMPTimeout(inp) {
    var id = inp.attr("id");
    var block_set_ver2_time = $("#settings_snmp_version2_alert_timeout");
    if (id == "snmp_type_trap") {
        block_set_ver2_time.slideUp("normal");
    } else {
        block_set_ver2_time.slideDown("normal");
    }
}
// инициализация валидатора
function checkFormSettingsSNMP() {
	$.validator.addMethod('integer', function(value, element) {
		var value = $(element).attr("value");
		var reg = /^[0-9]*$/;
		if (reg.test(value)) return true;
		return false;
	}, ERROR3 );
    $.validator.addMethod("checkUniqueValue", function(value, element) {
        var inpts = $("#sortable input[type=text]");
        var value = parseInt($(element).attr("value"));		
        var id = $(element).attr("id");
        var error = 0;
        $.each(inpts, function() {
            var value_cur = parseInt($(this).val());
            var id_cur = $(this).attr("id");
            if (value_cur && (id_cur != id) && (value_cur == value)) {
                error++;
            }
        });
        if (error > 0) return false;
        return true;
    }, ERROR3 );

    var validator = $("#formIntegration").validate({
        errorPlacement: function(error, element) {
            var id = $(element).attr("id");
            if (id == "snmp_common_upd") {
                $(element).parent().addClass("err_forms");
                error.appendTo( element.parent().parent().parent().parent().parent().prev() );
            } else if ($(element).attr("class").indexOf("inp_move") > -1) {
                error.appendTo( element.next() );
            } else {
                error.appendTo( element.parent().parent().prev() ); 
            }
        },
        submitHandler: function() {
			saveSettings('snmp');
        }        
    }); 
    var inp = $("input[name=system_control_snmp_need_alert]:checked");
    if (inp.attr("id") == "snmp_need_alert_yes") {
        addRulesSettingsSNMP();
    } 
}
// передать порядок полей для идентификации
function setIdentOrderSNMP() {
    var inp_order = $("#system_control_snmp_oid_identification_order");
    var inps = $("#sortable input[type=text]");
    var val_order = "";
    $.each(inps, function() {
        if ($(this).val()) {
            val_order = val_order + $(this).attr("name").split("system_control_snmp_oid_identification_")[1] + ","
        }
    });
    if (val_order) {
        val_order = val_order.substr(0, val_order.length - 1);
    }
    inp_order.val(val_order);
}
function getIdentOrderSNMP() {
    var inp_order = $("#system_control_snmp_oid_identification_order");
    var val_order = inp_order.val();
    var cont_add = $("#sortable_add");
    var cont = $("#sortable");
    var param = "";
	var inp;
    if (val_order) {
        var array_order = val_order.split(",");
        for (var i = 0; i < array_order.length; i++) {
			inp = $("#sortable input[name=system_control_snmp_oid_identification_" + array_order[i] + "]");
			if (inp.size() > 0) {
				param = inp.parent();
				cont_add.html(cont_add.html() + "<div class='block bl_param'>" + param.html() + "</div>");
				param.remove();			
			}
        } 
		cont_add.html(cont_add.html() + cont.html());
		cont.html(cont_add.html());
		cont_add.html("");                  
    }
}
// добавление правил для полей
function addRulesSettingsSNMP() {
    var inp_ver2 = $("input[name=system_control_snmp_trap_version]:checked");
    if (inp_ver2.attr("id") == "snmp_version2") {
        addRulesSettingsSNMPVersion2()
    }
    $("#snmp_common_upd").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });
    $("#snmp_oid_base").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });
}
// если выбрана версия2
function addRulesSettingsSNMPVersion2() {
    $("#snmp_ident").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });    
    $("#snmp_ident_person_id").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });
    $("#snmp_ident_person_name").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });
    $("#snmp_ident_person_photo").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });
    $("#snmp_ident_coeff").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });
    $("#snmp_ident_camera_ip").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });
    $("#snmp_ident_camera_type").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });
    $("#snmp_ident_time").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });
    $("#snmp_ident_image_camera").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });
    $("#snmp_ident_image_base").rules("add", {
        integer: true,
        checkUniqueValue: true,
        messages: {
            integer: ERROR2
        }
    });

    $("#system_control_snmp_identification_alert_timeout").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });                                         
}
// удаление правил для полей
function removeRulesSettingsSNMP() {
    var inp_ver2 = $("input[name=system_control_snmp_trap_version]:checked");
    if (inp_ver2.attr("id") == "snmp_version2") {                                    
        removeRulesSettingsSNMPVersion2();
    }
    $("#snmp_common_upd").rules("remove");
    $("#snmp_oid_base").rules("remove");

    $("#formIntegration input[type=text]").removeClass("err_forms");
    $("#formIntegration .bl_error").html("");   
}
function removeRulesSettingsSNMPVersion2() {
    $("#snmp_ident").rules("remove");

    $("#snmp_ident_person_id").rules("remove");
    $("#snmp_ident_person_name").rules("remove");
    $("#snmp_ident_person_photo").rules("remove");
    $("#snmp_ident_coeff").rules("remove");
    $("#snmp_ident_camera_ip").rules("remove");
    $("#snmp_ident_camera_type").rules("remove");
    $("#snmp_ident_time").rules("remove");
    $("#snmp_ident_image_camera").rules("remove");
    $("#snmp_ident_image_base").rules("remove");

    $("#system_control_snmp_identification_alert_timeout").rules("remove");

    $("#formIntegration #settings_snmp_version2 input[type=text]").removeClass("err_forms");
    $("#formIntegration #settings_snmp_version2 .bl_param .bl_enter .bl_address").removeClass("err_forms");
    $("#formIntegration #settings_snmp_version2 .bl_error").html("");    
    $("#formIntegration #settings_snmp_version2 .bl_error2").html("");  
}
// сообщение, если параметры успешно применены
function successMessage(show, txt) {
	var block = $(".message_action");
    if (show) {
		if (txt) block.html(txt);
        block.slideDown("normal");
        $("html").scrollTop(0);
    } else {
        block.slideUp("normal");
    }
}
// сообщение, если параметры не применены
function errorMessage(show, txt) {
	var block = $(".message_warning");
    if (show) {
		if (txt) block.html(txt);
        block.slideDown("normal");
        $("html").scrollTop(0);
    } else {
        block.slideUp("normal");
    }
}
// перезапуск УС
function initFuncsBtnSave(protocol) {
	$("input[name=save_settings]").click(function() {
		funcsBtnSave($(this), protocol);
	});
}
function saveSettings(protocol) {
	$("#save_settings1").attr("checked", "checked");
	funcsBtnSave($("#save_settings1"), protocol);
	changeWindow({id: 'win_reboot_offer_dialog', css: {width: '300px', height: '200px'}});
}
function funcsBtnSave(inp, protocol) {
	var btn_ok = $("#win_reboot_offer_dialog_btn_yes");
	btn_ok.unbind("click");													
	if (inp.attr("id") == "save_settings1") {
		btn_ok.bind("click", function() {
			closeChangeWindow('win_reboot_offer_dialog');
			save_settings(protocol);
		});													
	} else {
		btn_ok.bind("click", function() {
			closeChangeWindow('win_reboot_offer_dialog');
			save_and_reboot_settings(protocol);
		});				
	}						
}
// сохранение настроек без перезапуска
function save_settings(protocol) {	
	if (protocol == "snmp") setIdentOrderSNMP();
	var options = {
		data: {save: "True"},
		success: function(msg) {
			showIndicator(false);
			if (msg && msg.status) {                                                                   
				successMessage(true, SET_SAVE);
				setTimeout('successMessage(false)', TIME_SHOW_MESSAGE);
			} else {
				errorMessage(true, ERROR_GLOBAL);
				setTimeout('errorMessage(false)', TIME_SHOW_MESSAGE);                            
			}
		},
		error: function() {
			showIndicator(false);
			errorMessage(true, ERROR_GLOBAL);
			setTimeout('errorMessage(false)', TIME_SHOW_MESSAGE);                     
		}
	};
	showIndicator(true);
	$("#formIntegration").ajaxSubmit(options);
}
// сохранение настроек и перезапуск системы
function save_and_reboot_settings(protocol){
	if (protocol == "snmp") setIdentOrderSNMP();
	var options = {
		data: {save: "True"},
		success: function(msg) {
			showIndicator(false);
			if (msg && msg.status) {                                                                   
				reboot_system({type: 'save', hooks: {hook_success_save_and_reboot: 'save_and_reboot_ok()', hook_error_save_and_reboot: 'save_and_reboot_error()'}});
			} else {
				errorMessage(true, ERROR_GLOBAL);
				setTimeout('errorMessage(false)', TIME_SHOW_MESSAGE);                            
			}
		},
		error: function() {
			showIndicator(false);
			errorMessage(true, ERROR_GLOBAL);
			setTimeout('errorMessage(false)', TIME_SHOW_MESSAGE);                     
		}
	};
	showIndicator(true);
	$("#formIntegration").ajaxSubmit(options);
}
function save_and_reboot_ok() {
	successMessage(true, SET_SAVE_APPLY);
	setTimeout('successMessage(false)', TIME_SHOW_MESSAGE);
}
function save_and_reboot_error() {
	successMessage(true, SET_SAVE);
	errorMessage(true, ERROR_REBOOT);
	setTimeout('successMessage(false)', 2*TIME_SHOW_MESSAGE);
	setTimeout('errorMessage(false)', 2*TIME_SHOW_MESSAGE);
}

// инициализация функций для универсальных оповещений
function initUniversalAlerts() {
    $("input[name=system_control_external_need_alert]").click(function() {
		showSettings($(this), 'universal_alerts');
    });
	checkAlertUniversal();
	checkFormSettingsUniversal();	
}
// проверка включены или нет универсальные оповещения
function checkAlertUniversal() {
    var inp = $("input[name=system_control_external_need_alert]:checked");
    if (inp.attr("id") == "universal_alerts_yes") {
        $("#settings_universal_alerts").show();
    } else {
        $("#settings_universal_alerts").hide();
    } 
}

// инициализация валидатора
function checkFormSettingsUniversal() {
    var validator = $("#formIntegration").validate({
        errorPlacement: function(error, element) {
            error.appendTo( element.parent().parent().prev() ); 
        },
        submitHandler: function() {
			saveSettings('universal');
        }        
    });
    var inp = $("input[name=universal_alerts]:checked");
    if (inp.attr("id") == "universal_alerts_yes") {
        addRulesSettingsUniversal();
    }
}
// добавление правил для полей
function addRulesSettingsUniversal() {
    $("#script_videoanalytics").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });	
    $("#script_identification").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });	
    $("#system_control_external_identification_alert_timeout").rules("add", {
        required: true,
        messages: {
            required: ERROR1
        }
    });		
}
// удаление правил для полей
function removeRulesSettingsUniversal() {
	$("#script_videoanalytics").rules("remove");
	$("#script_identification").rules("remove");
	$("#system_control_external_identification_alert_timeout").rules("remove");
	
	$("#formIntegration input[type=text]").removeClass("err_forms");
    $("#formIntegration .bl_error").html("");
}