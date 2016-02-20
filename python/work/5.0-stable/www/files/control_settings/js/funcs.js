/*** current ***/
function _createElement(nameNode, attr) {
	var elem = document.createElement(nameNode);
	for (var i in attr) {
		if (i == '_class') {
			var attributte = document.createAttribute('class');
			attributte.nodeValue = attr[i];
		} else {
			var attributte = document.createAttribute(i);		
			attributte.nodeValue = attr[i];		
		}					
		elem.setAttributeNode(attributte);
	}
	return elem;
}
// импорт параметров, шаг №1, загрузка файла настроек
function importParameters() {
	var file = $("#importfile");
	file.val("");
	file.prev().html("");
	var btn_ok = $("#btn_import");
	var page = $("#select_page").val();
	if (page == "control_settings_default") {
		btn_ok.val("Импорт");
	} else {
		btn_ok.val("Далее");
	}
	changeWindow({id: 'win_import', css: {width: '300px', height: '200px'}});
}
// импорт параметров, шаг №1, проверка формы
function checkImportForm() {
	var validator = $("#ImportParamsForm").validate({
		rules: {
			importfile: {
				required: true
			}
		},
		messages: {
			importfile: {
				required: ERROR_FILE
			}				   
		},
		errorPlacement: function(error, element) {
			error.appendTo( element.prev()); 
		},		
		submitHandler: function() {
			closeChangeWindow('win_import');
			var page = $("#select_page").val();
			if (page == "control_settings_default") {
				importParameter("import");
			} else {
				$("input[name=import]:first").attr("checked", "checked");			
				changeWindow({id: 'win_import2', css: {width: '300px', height: '200px'}});
			}
		}													 
	});						
}
// импорт параметров, шаг №2, выбор варианта для импорта
function checkOptionImport() {
	closeChangeWindow('win_import2');
	var check = $("input[name=import]:checked");
	if (check.attr("id") == "import1") {
		importParameter("import");
	} else {
		importParameter("import_reboot");
	}
}
// импорт параметров, запрос к серверу
function importParameter(state){
	var options = {
	  url: "/control_settings/import_settings/",
	  type: "POST",
	  success: function(msg) {
			update_settings(state);
	  },
	  error: function(msg){
	      window.location.reload();
	  }	  
	};
	showIndicator(true);
	$("#ImportParamsForm").ajaxSubmit(options);
}
// импорт параметров, обновление настроек
function update_settings(state){
	$("#id_save").val("0");
	var page = $("#select_page").val();
	if (page == "control_settings_default") {var url = "/control_settings/default/";}
	else {var url = "/control_settings/settings/";} 
	var options = {
	  target: "#main_params_content",
	  url: url,
	  type: "POST",
	  success: function(msg) {
			create_params_list(allparams);
			showIndicator(false);
			if (state) {
				if (state == "import") {
					showMessage(IMPORT_SUCCESS);
				} else if (state == "import_reboot") {
					reboot_system("import");
				}
			}
	   },
	  error: function(msg){
		showIndicator(false);
		showMessage(IMPORT_ERROR);
	}
	};
	$("#MainParamsForm").ajaxSubmit(options);
}
/*** select and unselect element ***/
function overElem(elem, over_class) {
	var cur_class = "";
	if (elem.className) cur_class = rtrim(elem.className);
	elem.className = cur_class + " " + over_class;
}
function outElem(elem, over_class) {
	var cur_class = elem.className;
	if (cur_class) {
		if (cur_class.indexOf(over_class) > -1) elem.className = replace_string(elem.className, over_class, '');
	}
}
/*** window ***/
function checkOpacity(obj, valueOpacity) {
	var browserType = navigator.userAgent.toLowerCase();
	if (browserType.indexOf('msie') >= 0) {
		obj['filter'] = 'alpha(opacity=' + valueOpacity*100 + ')';
	} else {
		obj['opacity'] = valueOpacity;
	}
}
function createTitleWindow(param) {
	var distX = 0;
	var distY = 0;
	if (param.distX) {
		distX = param.distX;
	}
	if (param.distY) {
		distY = param.distY;
	}
	var win = byId(param.id);
	var content = byId(param.id+'_contWF');
	content.innerHTML = param.txt;
	var w1 = param.width;
	var h1;
	win.style.width = w1 + 'px';
	checkOpacity(win, 0);
	win.style.display = 'block';
	if (param.height) {
		h1 = param.height;
		win.style.height = param.height + 'px';
	} else {
		h1 = win.offsetHeight;
	}
	win.style.display = 'none';
	var scr = screenSize();
	win.style.position = 'absolute';		
	win.style.left = positionScreen(param.elem, {w: w1, h: h1, distX: distX, distY: distY}).left +'px';
	var t = win.style.top = positionScreen(param.elem, {w: w1, h: h1, distX: distX, distY: distY}).top + getBodyScrollTop() +'px';
	checkOpacity(win, 1);
	win.style.display = 'block';
}
function hideTitle(id) {
	if (byId(id)) {
		byId(id).style.display = 'none';
	}
}
function showRebootWindow(param) {
	changeWindow({id: param.id, css: {width: '300px', height: '200px'}, txt: REBOOT_SYSTEM_ANSWER});
}
function saveSettingsAll() {
	$("#save_settings1").attr("checked", "checked");
	clockBtnSaveAll($("#save_settings1"));
	changeWindow({id: 'win_reboot_offer_dialog', css: {width: '300px', height: '200px'}});
}
function initFuncsSettingsAll() {
	$("input[name=save_settings]").click(function() {
		clockBtnSaveAll($(this))
	});
}
function clockBtnSaveAll(inp) {
	var btn_ok = $("#win_reboot_offer_dialog_btn_yes");
	btn_ok.unbind("click");													
	if (inp.attr("id") == "save_settings1") {
		btn_ok.bind("click", function() {
			closeChangeWindow('win_reboot_offer_dialog');
			save_settings();
		});													
	} else {
		btn_ok.bind("click", function() {
			closeChangeWindow('win_reboot_offer_dialog');
			save_and_reboot_settings();
		});				
	}						
}
/*** params list ***/
var count_li=0;
function create_params_list(allparams){
	if (allparams && (allparams.length > 0)){
		n = allparams.length;
		i = 1;
		cross = "params_content";
		iscross = true;
		while( i<n ) {
			cross_old = cross;
			if (i<n-1){cross = p_cross(allparams[i]["name"], allparams[i+1]["name"]);}
			cross_split = allparams[i]["name"].split(".");
			if (cross == ""){cross = "params_content";}
			obj = get_el(cross);
			if (!obj){
					cross_split = cross.split(".");
					ci = 0;                    
					sc = "";
					sc_prev = "params_content";
					while (ci<cross_split.length){  
					    sc_old = sc;                      
						if (sc != ""){sc += ".";}                        
						sc += cross_split[ci];
						objc = get_el("ul_"+sc);
						if (!objc){
							create_ul(sc_prev, sc, cross_split[ci], sc_old);
							create_li(sc_prev, sc);
						}else{
							objc = get_el(sc);
							if (!objc){
								create_li(sc_prev, sc);
							}
						}                     
						sc_prev = sc; 
						ci += 1;
					}
					create_div(sc_prev, allparams[i]);
			}else{
				create_div(cross_old, allparams[i]);
			}
			i += 1;
		} 
	}
}

function get_el(el){
	return document.getElementById(el);
}

function create_ul(parent, li_id, ind, sc_old){
	parnt = get_el(parent);   
	if (parnt){      
		oElement_UL = document.createElement("UL");
		if (parent == "params_content") oElement_UL.className = "settings_cont";		
		oElement_UL.id = "ul_"+li_id;
		if (!isNaN(parseInt(ind, 10))){
		    var childrens = parnt.childNodes;
		    if (childrens){
		        var i = 0;
		        var s;		        
        	    while (i < childrens.length){
        	        s = parseInt(childrens[i].id.replace("ul_"+sc_old+".", ""), 10);
                    if (s > parseInt(ind, 10)){
	                    parnt.insertBefore(oElement_UL, childrens[i]);
                        return true;
		            }
		            i += 1;
		        }
		    }
		}
		parnt.appendChild(oElement_UL);
	}        
}
function showWindowParameter(e) {
	if (!e) e = window.event;
	var el = (e.target) ? e.target : e.srcElement;
	addParameter({txt: el.name});
}
function showWindowDeleteParameter(e) {
	if (!e) e = window.event;
	var el = (e.target) ? e.target : e.srcElement;
	deleteParameter({txt: el.name.split("_")[0], head: true});	
}
function delParameter(name, head) {
	var txt = createTextMessage({name_block: "param_del", name: name, head: head});
	byId("delete_param_name").value = name;
	changeWindow({id: 'win_del', css: {width: '300px', height: '200px'}, txt: txt});	
}
function editParameter(name, head) {
	var txt = createTextMessage({name_block: "param_edit", name: name, head: head});
	var rename = byId("new_name_param");
	rename.value = name;
	byId("rename_param_name").value = name;
	changeWindow({id: 'win_edit', css: {width: '300px', height: '200px'}, txt: txt});
	setCaretTo(rename, name.length);
}
function KeyRenameParams(event){
    if ((event.charCode) ? event.charCode : event.keyCode == 13) {renameParameters(); closeChangeWindow('win_edit');}
}

function duplParameter(name, type) {
	var txt = createTextMessage({name_block: "param_dupl", name: name, type: type});
	byId("copy_param_name").value = name;
	var rename = byId("copy_new_name_param");
	rename.value = name;	
	changeWindow({id: 'win_dupl', css: {width: '300px', height: '200px'}, txt: txt});
	setCaretTo(rename, name.length);
}
function exportParameters() {
	var txt = createTextMessage({name_block: "param_exp"});
	changeWindow({id: 'win_export', css: {width: '300px', height: '200px'}, txt: txt});
}
function get_settings_name(li_id, operation){
	re_balancer = /^balancer\.\d+$/;
	if (li_id == "balancer"){        
		switch (operation){
			case "add": return ADD_BALANS;
			case "del": return DEL_ALL_BALANS;
			case "copy": return DUP_BALANS;
			case "rename": return RENAME_SET_BALANS;
			default: return BALANSS + " (" + ONLY + ": <span id='count_balancer'>0</span>)";
		}
	}else if (li_id == "control"){ 
		switch (operation){
			case "add": return ADD_SET_US;
			case "del": return DEL_ALL_SET_US;
			case "copy": return DUP_SET_US;
			case "rename": return RENAME_SET_US;
			default: return SET_US;
		}        
	}else if (li_id.match(re_balancer)){
		switch (operation){
			case "add": return ADD_SET_TO_BALANS;
			case "del": return DEL_BALANS;
			case "copy": return DUP_BALANS;
			case "rename": return RENAME_SET_BALANS;
			default: return BALANS;
		}    
	}else{
		switch (operation){
			case "add": return ADD_PARAM;
			case "del": return DEL_PARAM;
			case "copy": return DUP_PARAM;
			case "rename": return RENAME_PARAM;
			default: return li_id;
		}        
	}
	return li_id;
}

function create_li(parent, li_id){
	parnt = get_el("ul_"+li_id);   
	if (parnt){      
		oElement_LI = document.createElement("LI");
		div_s = "";
		if (parent == "params_content"){ 
			oElement_LI.className = "out";
			c = get_el(parent).childNodes.length-1;            
		}
		//oElement_DIV = document.createElement("DIV");
		//oElement_DIV.className = "name";

		var linkClassName = "link_head";
		oElement_LI.innerHTML += "<div onmouseout='javascript:outSettings(this, \"set_act\", \""+li_id+"\");' onmouseover='javascript:overSettings(this, \"set_act\", \""+li_id+"\");' id='div_"+li_id+"'></div>";
		parnt.appendChild(oElement_LI);		
		oElement_DIV = byId("div_"+li_id);      
		li_name = li_id;  
		div_style = "block"; 
		if (parent == "params_content"){
			if (c>0){
				div_style = "none";
				linkClassName = "link_head arrow_left";
			}
			li_name = get_settings_name(li_id);
		}					 
		re_balancer = /^balancer\.\d+$/;
		var re_daemon = /^balancer\.\d+\.daemon\..*/;
		var type = 'other';		
		if (li_id.match(re_balancer)){
			count_li += 1;
			byId("count_balancer").innerHTML = count_li; 
			div_s += "<span class='number'>"+count_li+".</span>";
			type = 'balancer';
		} else if (li_id.match(re_daemon)){
			type = 'daemon';
		}
		div_s += "<a onclick='javascript: showSettings(this, \""+li_id+"\"); return false;' class='"+linkClassName+"' href='#' id='link_"+li_id+"'";
		if (parent == "params_content"){
			div_s += " style='font-weight: bold';";
		}		
		div_s += ">"+li_name+"</a>";
		div_s += "<span style='visibility: hidden;' id='btn_"+li_id+"'>";
		if (parent != "params_content"){
			div_s += "<input type='button' title='"+get_settings_name(li_id, "copy")+"' class='btn_dupl' onClick='javascript: duplParameter(\""+li_id+"\", \""+type+"\");' value='' name=''/><input type='button' title='"+get_settings_name(li_id, "rename")+"' class='btn_edit' onClick='javascript: editParameter(\""+li_id+"\", true);' value='' name=''/>";
		}		    
		div_s += "<input type='button' title='"+get_settings_name(li_id, "add")+"' class='btn_add' value='' name='' onclick='javascript: addParameter({txt: \""+li_id+"\"});'/><input type='button' title='"+get_settings_name(li_id, "del")+"' class='btn_del' onClick='javascript: delParameter(\""+li_id+"\", true);' value='' name=''/></span>";
		oElement_DIV.innerHTML = div_s;

		oElement_DIV1 = _createElement("DIV", {id: li_id, _class: "selection"});
		oElement_DIV1.style.display = div_style;
		oElement_LI.appendChild(oElement_DIV1);		
	}
}
function outElem2(e) {
	//alert("nn");
	//outElem(this, 'act_set');
	if (!e) e = window.event;
	var el = (e.target) ? e.target : e.srcElement;
	if ((el.className) && (el.className == "list_block")) {
		outElem(el, 'act_set');
	}	
}
function overElem2(e) {
	//alert("nn");
	//overElem(this, 'act_set');"

	if (!e) e = window.event;
	var el = (e.target) ? e.target : e.srcElement;
	//alert(el.className);
	if ((el.className) && (el.className == "list_block")) {
		overElem(el, 'act_set');
	}	
}
function create_div(parent, obj){
	div_id = obj["name"];
	type = obj["type"];
	val = obj["val"];
	min = obj["min"];
	max = obj["max"];
	step = obj["step"];
	info = obj["info"];
	error = obj["error"];
	permit = obj["permit"];
	parnt = get_el(parent);
	if (parnt){
		oElement = parnt;     
		div_s = "";
		if (parent == "params_content"){ 
			c = get_el(parent).childNodes.length-1;
			//div_s += "<span>"+count_li+".</span>";                                   
		}
		divid = div_id
		if (byId(divid)) divid += "_1";
		div_s += "<div class='inner_cont' id='param_"+divid+"' onMouseOver='javascript:overSettings(this, \"set_act\", \""+divid+"\");' onMouseOut='javascript:outSettings(this, \"set_act\", \""+divid+"\");'>";
		div_s += "<div class='txt_param'><label for='"+divid+"'>"+div_id+":</label></div>";
		div_s += "<div class='inner_enter'>";
		div_s += "<div class='block_ie'>";
		div_s += "<div class='block'>";
		div_s += "<div class='inner_enter_add'>";               
 
        if (permit == "True"){
			div_s += val;			
			//div_s += "<input type='button' name='' value='' class='btn_help' onclick='update_settings();' />";
			div_s += "<span style='display: none;' id='btn_"+divid+"'>";     		
	    	div_s += "<input type='button' name='' value='' class='btn_add' title='"+get_settings_name(div_id, "add")+"' onClick='javascript: addParameter({txt: \""+div_id+"\"});' />";
	    	div_s += "</span>";		    
		}else{
		if (type == 0){
			div_s += "<input type='text' style='width: ";
			if (val.length >= val_length) div_s += max_length;
			else div_s += min_length;            
			div_s += "px;' value='"+val+"' id='"+divid+"' name='"+div_id+"' class='inp_txt inp_address'/>";
			obj["obj_id"] = divid; 
		}else if (type == 1){
		    obj["obj_id"] = "id"+div_id;
			div_s += "<input type='radio' class='inp_check' value='true' name='"+div_id+"' id='id"+div_id+"'";
			if (val == "true"){ div_s += " checked='checked'";}
			div_s += "/><label for='id"+div_id+"'>" + TURN_ON + "</label>";
			div_s += "<input type='radio' class='inp_check dist_left' value='false' name='"+div_id+"' id='idno"+div_id+"'";
			if (val == "false"){ div_s += " checked='checked'";}
			div_s += "/><label for='idno"+div_id+"'>" + TURN_OFF + "</label>";            
		}else{
		    obj["obj_id"] = divid;
			div_s += "<div class='spinbox'>";
			div_s += "<input type='text' onblur='javascript: checkSpin(this, "+val+", "+min+", "+max+");' style='width:55px;' class='inp_txt' value='"+val+"' name='"+div_id+"' id='"+divid+"'/>";
			div_s += "<div class='spinbtns'>";
			div_s += "<input type='button' onmouseup='javascript: clearTimer();' onmousedown=\"javascript: spinButton('up', "+min+", "+max+", "+step+", '"+divid+"');\" class='btnSpUp upU' value='' name=''/>";
			div_s += "<input type='button' onmouseup='javascript: clearTimer();' onmousedown=\"javascript: spinButton('down', "+min+", "+max+", "+step+", '"+divid+"');\" class='btnSpDown upD' value='' name=''/>";
			div_s += "</div>";
			div_s += "<script type='text/javascript'>params['"+div_id+"'] = '"+val+"';</script>";
			//div_s += "<input type='button' onmouseout=\"javascript: hideTitle('win_help_param');\" onmouseover=\"javascript: showHelpParam(this, {min: "+min+", max: "+max+"});\" value='' name='' class='btn_help'/>";
			div_s += "</div>";
		}        
		//div_s += "<input type='button' name='' value='' class='btn_help' onclick='update_settings();' />";
		div_s += "<span style='display: none;' id='btn_"+divid+"'><input type='button' name='' value='' class='btn_edit' title='"+get_settings_name(div_id, "rename")+"' onClick='javascript: editParameter(\""+divid+"\", false);' />";
		div_s += "<input type='button' name='' value='' class='btn_add' title='"+get_settings_name(div_id, "add")+"' onClick='javascript: addParameter({txt: \""+div_id+"\"});' />";
		div_s += "<input type='button' name='' value='' class='btn_del' title='"+get_settings_name(div_id, "del")+"' onClick='javascript: delParameter(\""+divid+"\", true);' /></span><span class='block_error'></span>";
		}
		div_s += "</div>";
		div_s += "<div id='help_"+divid+"' style='margin-left: 135px;'>"+info+"</div>";
		div_s += "</div></div></div></div>";
		oElement.innerHTML += div_s;
		//parnt.appendChild(oElement);
		//addEvent(oElement, 'mouseout', outElem2);
		//addEvent(oElement, 'mouseover', overElem2);        
	}
}

function p_cross(p1, p2){
	ok = true;
	s = 0;
	arr1 = p1.split(".");
	arr2 = p2.split(".");
	j = 0;
	while(ok){
	   ok = arr1[j]==arr2[j];
	   if (ok){s += arr1[j].length+1;}
	   j += 1;
	}
	return p1.substr(0, Math.max(0, s-1));
}

function add_new_param(){
	param_value0 = '' ;
	if (document.getElementById("param_value0")){
		param_value0 = document.getElementById("param_value0").value;
	}
	param_value1 = '';
	if (document.getElementById("radio_default_ok")){
		param_value1 = document.getElementById("radio_default_ok").checked;
	}	
	param_value2 = '';
	if (document.getElementById("param_value2")){
		param_value2 = document.getElementById("param_value2").value;
	}
	param_info = '';
	if (document.getElementById("param_info")){
		param_info = document.getElementById("param_info").value;
	}		
	param_name = '';
	if (document.getElementById("name_param")){
		param_name = document.getElementById("name_param").value;
	}		
	min_val = '';
	if (document.getElementById("min_val")){
		min_val = document.getElementById("min_val").value;
	}		
	max_val = '';
	if (document.getElementById("max_val")){
		max_val = document.getElementById("max_val").value;
	}		
	step = '';
	if (document.getElementById("step")){
		step = document.getElementById("step").value;
	}			
	type = '';
	if (document.getElementById("type_param")){
		type = document.getElementById("type_param").value;
	}			
	base = '';
	if (document.getElementById("base")){
		base = document.getElementById("base").value;
	}
	$.ajax({
		type: "POST",
		url: "/control_settings/add_param/",
		data: {min_val:min_val,max_val:max_val,step:step,param_info:param_info,param_value0:param_value0,param_value1:param_value1,param_value2:param_value2,param_name:param_name,type:type, base:base},
		success: function(msg){
			if (msg!="True"){
				ue = msg.split(";");
				if (ue.length==1) alert(msg);
				i = 0;
				while (i<ue.length){
					if (document.getElementById(ue[i])) { 
						document.getElementById(ue[i]).innerHTML = ue[i+1];
						byId(ue[i]).style.display = "block";
					}
					i += 2;
				}
			}
			else{				
				closeChangeWindow('win_add');
				update_settings();
			}
		},
		error: function(msg){	
		}
	});
}

function delete_param(){
	byId("delete_base_name").value = document.getElementById("base").value;

	var options = {
	  url: "/control_settings/delete_param/",
	  type: "POST",
	  success: function(msg) {
			showIndicator(false);
			if (msg!="True"){   		    
				showMessage(ERROR1);
			}
			else {
//				document.getElementById("param_" + document.getElementById("delete_param_name").value).style.display = 'none';
				showMessage(SUCCESS1);
				update_settings();
			}		  
	  },
		error: function(msg){
			showIndicator(false);
			showMessage(ERROR1);						
		}
	};
	showIndicator(true);
	$("#MainDeleteForm").ajaxSubmit(options);	
}

function save_settings(){
	byId("id_save").value = "1";	
	var options = {	  
	  url: "/control_settings/save_settings/",
	  type: "POST",
	  success: function(msg) {
			showIndicator(false);
			if (msg == "True") { showMessage(SUCCESS2); }
			else { showMessage("<div class='error'>" + ERROR2 + "</div>"); }
	  },
	  error: function(msg) {
	      showIndicator(false);
	      showMessage("<div class='error'>" + ERROR2 + "</div>");
	  }
	};
	showIndicator(true);
	$("#MainParamsSaveForm").ajaxSubmit(options);
}

function save_and_reboot_settings(){
	byId("id_save").value = "1";	
	var options = {	  
	  url: "/control_settings/save_settings/",
	  type: "POST",
	  success: function(msg) {
	  		showIndicator(false);
			reboot_system('save');
	  },
	  error: function(msg){
		 showIndicator(false);
		 showMessage("<div class='error'>" + ERROR3 + "</div>");
	  }
	};
	showIndicator(true);
	$("#MainParamsSaveForm").ajaxSubmit(options);
}

function exportParameter(){
        location.replace('/control_settings/export_settings/');
        /*
	var options = {
	  url: "/control_settings/export_settings/",
	  type: "POST",
	  success: function(msg) {
			location.replace(msg);
	  },
	  error: function(msg){
	      window.location.reload();
	  }	
	};
	showIndicator(true);
	$("#MainParamsForm").ajaxSubmit(options);
	*/
}



function renameParameters(){
	byId("rename_base_name").value = document.getElementById("base").value;
	var options = {
	  url: "/control_settings/rename_param/",
	  type: "POST",
	  success: function(msg) {
			if (msg == "True") {
				showMessage(SUCCESS3);
				showIndicator(false);
				update_settings();				
			}									
			else if (msg=="Not all"){
				showMessage(ERROR4);
				showIndicator(false);
				update_settings();										
		    }else{   		    
				showMessage(ERROR5);
				showIndicator(false);
			}
  
	  },
		error: function(msg){
			showMessage(ERROR5);
			showIndicator(false);			
		}	  
	};
	showIndicator(true);
	$("#MainRenameForm").ajaxSubmit(options);
}

function copyParameters(){
	byId("copy_base_name").value = document.getElementById("base").value;
	var options = {
	  url: "/control_settings/copy_param/",
	  type: "POST",
	  success: function(msg) {
			if (msg!="True"){   		    
				showMessage(ERROR6);
				showIndicator(false);
			}
			else {
				showMessage(SUCCESS6);
				update_settings();
			}		  
	  },
		error: function(msg){
			showMessage(ERROR6);
			showIndicator(false);			
		}	  
	};
	showIndicator(true);
	$("#MainCopyForm").ajaxSubmit(options);
}

function searchSettings(){
    var ss = byId("search_settings");
	if (allparams && ss){
	    var sw = ss.value.split(" "); 
		var n = allparams.length;
		var i = 1;
		var cross = "params_content";
		while( i<n ) {
		    for ( var j = 0, len = sw.length; j < len; ++j ) {
		        swi = sw[j];
		        indx_i = allparams[i]["val"].indexOf(swi);  
		        if (indx_i>=0 && allparams[i]["obj_id"]){
		            obj = byId(allparams[i]["obj_id"]);
		            if (obj){		     
		                var names = allparams[i]["name"].split(".");		                
		                for ( var k = 0, lenk = names.length; k < lenk; ++k ) {
		                }
		                while (indx_i>=0){
		                    indx_end = indx_i+swi.length;
		                    if(obj.createTextRange) { 
		                        var range = obj.createTextRange();
		                        range.collapse(true); 
		                        range.moveStart("character", indx_i);
    	                        range.moveEnd("character", indx_end);                    		             
		                        range.select(); 
	                        } else if(obj.setSelectionRange) {
	                            if (obj.style.display != "none"){
	                            obj.focus();			                                  
	                            obj.setSelectionRange(indx_i, indx_end);
	                            }		                  
                            }                            
                            indx_i = allparams[i]["val"].indexOf(swi, indx_end);
                        }
		            }
		        }
		    }
		    i++;
		}
	}
}