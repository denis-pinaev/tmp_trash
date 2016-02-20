function showCamera(btn, count, nameCamera, numCamera) {
	var communicator = getInfoCommunicator();
	var curr_class = btn.className;
	if (curr_class.indexOf('play') > -1) {
		initButtonCamera(count);
		btn.className = 'btn_camera stop_act';
		showNameCamera(nameCamera);
		byId("mini_camera_info").style.display = 'none';
		//byId("mini_camera").style.display = 'block';		
		//byId('mini_camera').innerHTML = addFlash(numCamera, communicator.host, communicator.port);

	} else {
		btn.className = 'btn_camera play_act';
		showNameCamera('&nbsp;');
		byId("mini_camera_info").style.display = 'block';
		//byId("mini_camera").style.display = 'none';	
		//byId("mini_camera").innerHTML = '&nbsp;';		
	}
}
function getInfoCommunicator() {
	var list = byId('select');
	if (list.selectedIndex != -1) {
		var value = list.options[list.selectedIndex].text;
		var i = value.indexOf(':');
		var host = value.substr(0, i);
		var port = value.substr(i+1, value.length);
		return {host: host, port: port};
	}
}
function showLearnCameraBlock(show) {
    if (show) {
        byId('choose_person').style.display = 'none';
        byId('learn_camera').style.display = 'block';
    } else {
        byId('learn_camera').style.display = 'none';
        byId('choose_person').style.display = 'block';
    }
}
function showListCamera(link, url) {
    var check = checkChoosePerson();
    if (check) {
        link.href = url;
    } else {
        return false;
    }
}

function getChooseCamera() {
    var radioObj = document.frm_learn.video;
    if (radioObj){
    if (radioObj.length) {
        for (var i = 0; i < radioObj.length; i++) { 
            if (radioObj[i].checked) {
                return {num: radioObj[i].value, numId: i+1}; 
            }
        }
    } else { 
        return {num: radioObj.value, numId: 1}; 
    }
    }else{
        return {num: -1, numId: 0};
    }
    
}

function showChooseCamera() { 
    var info = getChooseCamera(); 
    if (info) {
        var numCamera = info.num;
        if (numCamera>=0){ 
        var communicator = getInfoCommunicator(); 
        var nameCamera = byId('info' + info.numId).innerHTML; 
        showNameCamera(nameCamera);
        byId("mini_camera_info").style.display = 'none'; 
        byId("mini_camera").style.display = 'block';
        if (flashVersion()) {
            byId('mini_camera').innerHTML = addFlash(numCamera, communicator.host, communicator.port); 
        } else {
            byId('mini_camera').innerHTML = '<div class="noFlash">У вас отсутствует или установлена старая версия flash плеера. Новую версию плеера можно скачать <script src="/files/js/person/funcs.js" type="text/javascript"></script><a target="_blank" href="http://get.adobe.com/flashplayer/">здесь</a></div>';
        }
        }
    }
}
function showLearnCamera(link, url, person) {
    var num = getChooseCamera().num;
    if (num) {
        link.href = url + num + person;
    } else {
        return false;
    }
}

function chooseCamera(num, nameCamera, numCamera) {
    byId('choose'+num).checked = 'checked';
    var communicator = getInfoCommunicator(); 
    showNameCamera(nameCamera);
    byId("mini_camera_info").style.display = 'none'; 
    byId("mini_camera").style.display = 'block';
    byId('mini_camera').innerHTML = addFlash(numCamera, communicator.host, communicator.port); 
}

function selectRow(tr, num) { 
    var cur_class = ""; 
    if (tr.className) {
        cur_class = rtrim(tr.className); 
    }
    tr.className = cur_class + " act"; 

    var btn = byId("btn_play"+num); 
    if (btn) {
        var btn_class = btn.className;
        btn.className = btn_class + "_act"; 
    } 
} 

function unselectRow(tr, num) {
    if (tr.className.indexOf('odd') != -1) { 
        tr.className = "odd"; 
    } else {
        tr.className = ""; 
    } 

    var btn = byId("btn_play"+num); 
    if (btn) {
        var btn_class = btn.className;
        var i = btn_class.indexOf('_act');
        btn.className = btn_class.substr(0, i); 
    } 
} 

function checkAllPhotos(inp, count, start, finish) { 
    var num = Math.min(count, finish); 
    if (inp.id == 'choose_all') {
        byId('choose_all2').checked = inp.checked; 
    } else {
        byId('choose_all').checked = inp.checked; 
    }
    var check;
    for (var i = 1; i <= num; i++) { 
        check = byId('check'+i); 
        if (check){
            if (inp.checked) { 
               check.checked = true;
               searchElem(check, 'LI').className = 'act'; 
            } else {
               check.checked = false;
               searchElem(check, 'LI').className = ''; 
            } 
        } 
    } 
} 

function checkAllPhotosBtn(id, count, start, finish) { 
    var num = Math.min(count, finish); 
    var inp = byId(id);
    inp.checked =  (inp.checked == false) ? 'checked' : false; 
    if (inp.id == 'choose_all') {
        byId('choose_all2').checked = inp.checked; 
    } else {
        byId('choose_all').checked = inp.checked; 
    }
    var check;
    for (var i = 1; i <= num; i++) { 
        check = byId('check'+i); 
        if (check){
            if (inp.checked) { 
               check.checked = true;
               searchElem(check, 'LI').className = 'act'; 
            } else {
               check.checked = false;
               searchElem(check, 'LI').className = ''; 
            } 
        } 
    } 
} 

function checkPhoto3(inp, count, start, finish) { 
    var li = searchElem(inp, 'LI'); 
    if (inp.checked) {
        li.className = 'act';
        var num = Math.min(count, finish); 
        checkAllElem(num, start); 
    } else {
        li.className = '';
        byId('choose_all').checked = false; 
        if (byId('choose_all2')) {
            byId('choose_all2').checked = false; 
        } 
    } 
} 

function showMessageExport(count, name_block) {
    var txt;
    var head;
    var check = isChecked(count);
    if (check) {
        txt = createTextMessage({name_block: name_block+"_export", count: check});
        changeWindow({id: 'win_export', css: {width: '300px', height: '200px'}, txt: txt});
    } else {
        txt = createTextMessage({name_block: name_block});
        changeWindow({id: 'win_mess', css: {width: '300px', height: '200px'}, txt: txt});
    }
}

function clickDelete(count) {
    closeChangeWindow('win_del');
    var obj = getValueIsChecked(count);
    var res = '';
    for(var i = 0; i<obj.c; i++){ 
        if (i!=0){
            res=res+',';
        }
        res = res + obj.array[i]; 
    }
    return res; 
}