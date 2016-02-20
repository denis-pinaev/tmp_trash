$(function() {
    initAddIP();
});
// инициализация функций
function initAddIP() {    
    $("#link_add_ip").click(function() {
        addIP();
        return false;
    });
    $("#ip0").attr("value", "");
    $("#ip0").focus();
    $("#ip0").bind("change keyup", function() {
        errorMessage(false);
        if (checkLightIP($("#ip0"))) {
            lockButton(false);
        }
    });
    $("#btn_add").click(function() {
        if (checkAllIP()) {
            AddIpList(getIP());
        }
    });
}
function AddIpList(ip_list) {    
    errorMessage(false);
    $.ajax({
        url: URL_ADD_IP,//'/settings/web_api/	
        type:'POST',
        dataType: 'json',
        data: 'ip_list='+$.toJSON(ip_list) + "&user_login=" + USER,
        beforeSend: function(){
            //крутяшку включаем                                    
        },
        success: function(msg) {
            //отключаем крутяшку
            obj = eval(msg);
            if (obj && obj.status){
                if (obj.status in ERR){
                    errorMessage(true, ERR[obj.status]);
                } else {
                    errorMessage(true, ERROR_MESSAGE3);
                } 
                setTimeout('errorMessage(false)', 3000);
            } else if (obj && (obj.result)) {  
        		if (obj.result.length > 1){
        			successMessage(true, SUCCESS_MESSAGE + ' ' + obj.result.toString(), countIP);
        		}else{
        			successMessage(true, SUCCESS_MESSAGE2 + ' ' + obj.result.toString(), countIP);
        		}               
                setTimeout('clearFormIP()', 3000);
            }        
        },
        error: function() {
            //отключаем крутяшку
            errorMessage(true, ERROR_MESSAGE2);
            setTimeout('errorMessage(false)', 3000);
        } 
    });
}
// добавление блока ввода IP
function addIP() {
    var block = $("#content_ip");
    var count = block.children("div.form_block").size();
    var ip = '<div class="form_block" style="display: none;"><div class="error_field"></div>';
    ip += '<input class="inp_txt dist_left_form" name="" type="text" value="" />';
    ip += '<input type="button" value="" name="" class="btn_delete" />';
    ip += '</div>';
    ip = $(ip);
    var ip_btn = ip.children("input[type=button]");
    var ip_inp = ip.children("input[type=text]");
    ip_btn.css("opacity", "0.2");
    ip_btn.click(function() {
        deleteIP($(this));
    });
    ip.mouseover(function() {
        showButtonDelete($(this), true);
    });
    ip.mouseout(function() {
        showButtonDelete($(this), false);
    });
    block.append(ip);
    ip.slideDown("normal", function() { ip_inp.focus();    });
    ip_inp.bind("change keyup", function() {
        errorMessage(false);
        if (checkLightIP(ip_inp)) {
            lockButton(false);
        }    
    });    
}
// удаление блока ввода IP
function deleteIP(btn) {
    var block = btn.parent();
    block.slideUp("normal", function() { block.remove() });
}
// кнопка удаления блока ввода IP
function showButtonDelete(obj, show) {
    var btn = obj.children("input[type=button]");
    if (show) {
        btn.css("opacity", "1")
    } else {
        btn.css("opacity", "0.2")
    }
}
// лёгкая проверка на корректность IP
function checkLightIP(ip) {
    //alert(" check ip ");
    var ip_get = ip.attr("value");
    var ip_tested = /^ *[0-9]{1,3} *\. *[0-9]{1,3} *\. *[0-9]{1,3} *\. *[0-9]{1,3} *$/;
    if (ip_get.search(ip_tested) == -1) {
        return false;
    } else {
        return true;
    }    
}
// проверка на корректность IP
var ip_tested = /^ *(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])( *\. *(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])){3} *$/;
function checkIP(ip) {
    var ip_get = ip.attr("value");

    if (ip_get.search(ip_tested) == -1) {
        return false;
    } else {
        return true;
    }
}
function checkIP2(ip) {
    var ip_get = ip.attr("value");
    if (ip_get.search(ip_tested) == -1) {
        ip.addClass("error");
    } else {
        ip.removeClass("error");
        if (ip.attr("id") == "ip0") {
            ip.parent().parent().prev().html("");
        } else {
            ip.prev().html("");
        }
    }
}
// количество полей ввода IP
function countIP() {
    var ip_list = $("#content_ip").find("input[type=text]");
    return ip_list.size();
}
// проверка всех IP на корректность
function checkAllIP() {
    var ip_list = $("#content_ip").find("input[type=text]");
    var count_err = 0;
    $.each(ip_list, function(key, value) {
        var ip = $(this);
        var err = ip.prev();
        if (ip.attr("id") == "ip0") {
            err = ip.parent().parent().prev();
        }        
        if (!checkIP(ip)) {            
            ip.addClass("error");
            err.html(ERROR_MESSAGE);
            ip.bind("change keyup", function() {
                checkIP2($(this));
            });
            count_err++;
        }
    });
    if (count_err == 0) return true
    else return false;
}
// сообщения
function successMessage(show, msg, count) {
    if (show) {
        if (count) { $("#success_message").html(msg); } 
        else { $("#success_message").html(msg); }    
        $("#success_message").slideDown("normal");
        $("html").scrollTop(0);
    } else {
        $("#success_message").slideUp("normal");
    }
}
function errorMessage(show, msg) {
    if (show) {
        $("#error_message").html(msg);
        $("#error_message").slideDown("normal");
        $("html").scrollTop(0);
    } else {
        $("#error_message").slideUp("normal");
    }
}
// получить IP адреса
function getIP() {
    var ip_list = $("#content_ip div.form_block input[type=text]")
    var ip_arr = new Array();
    $.each(ip_list, function() {
        if ($(this).val()) {
            ip_arr.push($(this).val());    
        }    
    });
    return ip_arr;
}
// блокирование кнопки
function lockButton(lock) {
    var btn = $('#btn_add');
    if (lock) {
        btn.addClass('dis');
        btn.attr("disabled", "disabled");    
    } else {
        btn.removeClass('dis');
        btn.attr("disabled", false);    
    }
}
// очистить форму
function clearFormIP() {
    successMessage(false);
    $("#ip0").attr("value", "");
    $("#ip0").focus();
    var ips = $("#content_ip div.form_block").find("input[type=text]");
    $.each(ips, function(key, value) {
        if (key > 0) {
            $(this).parent().remove();
        }
    });
    lockButton(true);    
}