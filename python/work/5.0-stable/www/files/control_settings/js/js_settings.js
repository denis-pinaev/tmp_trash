function showSettings(link, id_content) {
    /*var content = byId(id_content);
    if (content.style.display == 'block') {
        link.className = 'arrow_left';
        content.style.display = 'none';
    } else {
        link.className = 'link_head';
        content.style.display = 'block';
    }*/
    var content = byId(id_content);
    if (content.style.display == 'block') {
        link.className = link.className + ' arrow_left';
        content.style.display = 'none';
    } else {
        link.className = link.className.split('arrow_left')[0];
        content.style.display = 'block';
    }    
}
function showHelpParam(elem, params) {
    var content = '';
    var head = '';
    for (var i in params) {
        head = createTextMessage({name_block:i});
        content += '<div>' + head + params[i] + '</div>';
    }
    createTitleWindow({distX: 5, width: 300, elem: elem, id: 'win_help_param', txt: content});
}
function reboot_system(type){
    $.ajax({
        type: "GET",
        url: "/control_settings/rebootsystem/",
        data: {},
        success: function(msg){
            if (msg == "True") {
                if (type) {
					if (type == 'save') {
						showMessage(SET_SAVE_APPLY);
					} else if (type == 'import') {
						showMessage(SET_IMPORT_APPLY);
					}
                } else {
                    showMessage(REBOOT_SYSTEM);
                }             
            }
            else {
                if (type) {
					if (type == 'save') {
						showMessage(SET_SAVE + "<div class='error dist_top'>" + ERROR_REBOOT + "</div>");
					} else if (type == 'import') {
						showMessage(IMPORT_SUCCESS + "<div class='error dist_top'>" + ERROR_REBOOT + "</div>");
					}
                } else {
                    showMessage("<div class='error'>" + ERROR_REBOOT + "</div>");
                }              
            }
        },
        error: function(msg){
            if (type && (type == 'save')) {
                showMessage(SET_SAVE + "<div class='error dist_top'>" + ERROR_REBOOT + "</div>");
            } else {
                showMessage("<div class='error'>" + ERROR_REBOOT + "</div>");
            }
        }
    });
}
function addParameter(param) {
    setValueDefaultSelect("type_param");
    initBlocksType();
    initBlockError();
    byId("name_param").value = "";
    byId("type_text").style.display = "block";
    if (param && param.txt) {
        byId("name_param").value = param.txt;
    }
    changeWindow({id: 'win_add', css: {width: '550px', height: '280px'}});
}
function initBlocksType() {
    byId("win_add").style.height = "280px";
    byId("type_text").style.display = "none";
    byId("type_radio").style.display = "none";
    byId("type_spinbox").style.display = "none";
}
function initBlockError() {
    byId("error_param_name").style.display = "none";
    byId("error_type_param").style.display = "none";
    byId("error_param_value0").style.display = "none";
    byId("error_param_value1").style.display = "none";
    byId("error_param_value2").style.display = "none";
    byId("error_min_val").style.display = "none";
    byId("error_max_val").style.display = "none";
    byId("error_step").style.display = "none";
}
function changeTypeParams(select) {
    var select = byId(select);
    initBlocksType();
    if (select.selectedIndex == 0) {                          
        byId("type_text").style.display = "block";
    }
    if (select.selectedIndex == 1) {
        byId("type_radio").style.display = "block";
    }
    if (select.selectedIndex == 2) {
        byId("win_add").style.height = "380px";
        byId("type_spinbox").style.display = "block";
    }
}
function deleteParameter(param) {
    idp = byId("id_delete_parameter");
    if (idp) idp.value = param.txt;
    var txt = createTextMessage({name_block: "param_del", name: param.txt, head: param.head});
    changeWindow({id: 'win_del', css: {width: '300px', height: '200px'}, txt: txt});
}
function prevElem(obj, class_name) {
    var node = obj;
    do node = node.previousSibling
    while(node && (node.nodeType != 1) && (node.className != class_name));
    return node;    
}
function overSettings(elem, over_class, id_param) {
    var cur_class = "";
    if (elem.className) cur_class = rtrim(elem.className);
    elem.className = cur_class + " " + over_class;
    var help = byId("help_" + id_param);
    if (help) {
        byId("btn_" + id_param).style.display = "inline";
        help.style.marginLeft = prevElem(help, 'inner_enter_add').offsetWidth + 3 + 'px';
    } else {
        byId("btn_" + id_param).style.visibility = "visible";
    }
}
function outSettings(elem, over_class, id_param) {
    var cur_class = elem.className;
    if (cur_class) {
        if (cur_class.indexOf(over_class) > -1) elem.className = replace_string(elem.className, over_class, '');
    }
    var help = byId("help_" + id_param);
    if (help) {
        byId("btn_" + id_param).style.display = "none";
        help.style.marginLeft = prevElem(help, 'inner_enter_add').offsetWidth + 3 + 'px';
    } else {
        byId("btn_" + id_param).style.visibility = "hidden";
    }
}