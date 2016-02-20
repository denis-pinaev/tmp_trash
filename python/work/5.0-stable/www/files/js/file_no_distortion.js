var MAX_COUNT_FILE = 20

function showBlockFileUpload() {
    var upload = checkBrowserInfo();
    if (upload == 'single') {
        $("#upload_single_file").show();
        $("#file0").bind("change keyup", function() {
                if (checkFile($(this))) {
                    lockButton('btn_single_file', false);
                    setCountUploadFile();
                    addFile();
                }
        });
        $("#btn_single_file").click(function() {
            multipleUpload();
        });
    } else {
        $("#upload_multiple_file").show();
        $("#multiple_file").change(function() {
            multipleUpload();
        });
    }
}
function multipleUpload() {
    var form = $("#formUploadFile");
    form.submit();
    $("#block_faces").hide();
    $("#upload_multiple_file").hide();
	$("#block_message").hide();	
    $("#block_loader").show();
}
// проверка на тип и версию браузера
function checkBrowserInfo() {
    var br = $.browser;
    if (br) {
        if (br.msie) { 
            return 'single';
        }
        if (br.mozilla) {
            var browserType = navigator.userAgent.toLowerCase();
            var str1 = "firefox/";
            var pos1 = browserType.indexOf(str1) + str1.length;
            var pos2 = browserType.length;
            var ver = parseFloat(browserType.substr(pos1, pos2 - pos1));
            if (ver >= 3.6) {
                return 'multiple';
            } else {
                return 'single';
            }
        }
        if (br.opera) {
            var ver = parseFloat(br.version);
            if (ver >= 10.62) {
                return 'multiple';
            } else {
                return 'single';
            }
        }
        if (br.safari) {
            var browserType = navigator.userAgent.toLowerCase();
            var str1 = "version/";
            var str2 = "safari/";
            var str3 = "chrome/";
            if (browserType.indexOf(str3) > -1) {
                var pos1 = browserType.indexOf(str3) + str3.length;
                var pos2 = browserType.indexOf(str2);
                var ver = parseFloat(browserType.substr(pos1, pos2 - pos1));
                if (ver >= 8) {
                    return 'multiple';
                } else {
                    return 'single';
                }
            } else {
                var pos1 = browserType.indexOf(str1) + str1.length;
                var pos2 = browserType.indexOf(str2);
                var ver = parseFloat(browserType.substr(pos1, pos2 - pos1));
                /*if (ver > 4) {
                    return 'multiple';
                } else {*/
                    return 'single';
                //}
            }
        }
        return 'single';
    }
    return 'single';
}

// блокирование кнопки
function lockButton(id, lock) {
    var btn = $('#' + id);
    if (lock) {
        btn.addClass('noact_btn');
        btn.attr("disabled", "disabled");    
    } else {
        btn.removeClass('noact_btn');
        btn.attr("disabled", false);    
    }
}
// установить количество загруженных файлов
function setCountUploadFile() {
    if (getCountUploadFile()) {
        $("#current_count_file").html(getCountUploadFile());
    } else {
        $("#current_count_file").html("0");
    }
}
// получить количество загруженных файлов
function getCountUploadFile() {
    var block = $("#content_file");
    var files = block.find("div.form_block input[type=file]");
    var count = 0;
    $.each(files, function(key, value) {
        if ($(this).val()) {
            count++
        }
    });
    if (count > 0) return count;
    else return false;                              
}
// добавить файл
function addFile() {
    var block = $("#content_file");
    var count = block.children("div.form_block").size();
    var file_last = block.find("div.form_block input[type=file]:last");
    if ((count < MAX_COUNT_FILE) && (file_last.val())) {
        var file = '<div class="form_block" style="display: none;"><div class="error_field"></div>';
        file += '<input class="dist_left_form" name="file" type="file" value="" />';
        file += '<input type="button" value="" name="" class="btn_delete" />';
        file += '</div>';
        file = $(file);
        var file_btn = file.children("input[type=button]");
        var file_inp = file.children("input[type=file]");
        file_btn.css("opacity", "0.2");
        file_btn.click(function() {
            deleteFile($(this));
        });
        file.mouseover(function() {
            showButtonDelete($(this), true);
        });
        file.mouseout(function() {
            showButtonDelete($(this), false);
        });
        block.append(file);
        file.slideDown("normal");
        file_inp.bind("change keyup", function() {
            if (checkFile(file_inp)) {
                lockButton('btn_single_file', false);
                setCountUploadFile();
                addFile();
            }    
        });                               
    }
}
// удаление файла
function deleteFile(btn) {
    var block = btn.parent();
    block.slideUp("normal", function() { 
        block.remove();
        setCountUploadFile();
    });
}
// кнопка удаления блока
function showButtonDelete(obj, show) {
    var btn = obj.children("input[type=button]");
    if (show) {
        btn.css("opacity", "1")
    } else {
        btn.css("opacity", "0.2")
    }
}
// проверка на наличие значения
function checkFile(obj) {
    if (obj.val()) {
        return true;
    }
    return false;
}