var params = new Array();
function checkSpinEdit(obj) {
	//var re = /^-?\d+$/i;
	var re = /^-?\d+\.?\d{0,2}/i;
	if (obj.value) {
		var v = deleteSpace(obj.value);
		return re.exec(v);
	}
	return true;
}

function deleteSpace(s) {
	var v = s.replace(/^\s+/, '');
	v = v.replace(/\s+$/, '');
	return v;
}

function checkSpin(spinEdit, defaultValue, min, max) {
	if (!spinEdit.value) {
		spinEdit.value = defaultValue;
		return;
	}
	var check = checkSpinEdit(spinEdit);
	if (!check) {
		spinEdit.value = defaultValue;
		return;
	}
	if ((parseFloat(check) < min)) {
		spinEdit.value = min;
		return;	
	}
	if ((parseFloat(check) > max)) {
		spinEdit.value = max;
		return;	
	}	
	spinEdit.value = check;
}

function spinClick(direct, min, max, st, inpId) {
	var spinEdit = byId(inpId);
	if (spinEdit == null) return;

	checkSpin(spinEdit);

	var spinValue = parseFloat(spinEdit.value);
	var step = parseFloat(st);
	var round = 1000;

	if (direct == "up") {
		if (spinValue <= (max-step)) {
			var original = spinValue + step;
			spinEdit.value = Math.round(original*round)/round; 
		}
	} else {
		if (spinValue >= (min+step)) {
			var original = spinValue - step;
			spinEdit.value = Math.round(original*round)/round;
		}	
	}
}

var timer;
function spinButton(direct, min, max, st, inpId) {
	clearTimer();
	spinClick(direct, min, max, st, inpId)
	timer = window.setTimeout("spinButton('" + direct + "', '" + min + "', '" + max + "', '" + st + "', '" + inpId + "')", 200);	
}
function clearTimer() {
	clearTimeout(timer);
}

function addEvent(el, evType, handle) {
	var el = byId(el);
	if (el.addEventListener) {
			el.addEventListener(evType, handle, false);
	} else if (el.attachEvent) {
		// for ie
		el["e" + evType + handle] = handle;
		el[evType + handle] = function() {
			el["e" + evType + handle](window.event)
		}
		el.attachEvent("on" + evType, el[evType + handle]);
	}
}
