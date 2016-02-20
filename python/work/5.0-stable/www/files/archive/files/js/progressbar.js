var loopObject = {start:0, end:100, current:0, interval:null};
function calcProgress(current, total) {
	if (current <= total) {
		var factor = current/total;
		var pct = Math.ceil(factor * 100);
		byId("percent_w").innerHTML = pct + "%";
		if (current > 50) {
			byId("percent_b").style.zIndex = "1"
		}
		byId("percent_b").innerHTML = pct + "%";
		byId("active").style.width = parseInt(factor * 280) + "px";
	}
}
function runit() {
	if (loopObject.current <= loopObject.end) {
		calcProgress(loopObject.current, loopObject.end);
		loopObject.current += Math.random()*10;
		loopObject.interval = setTimeout("runit()", 100);
	} else {
		calcProgress(loopObject.end, loopObject.end);
		loopObject.current = 0;
		loopObject.interval = null;
		closeChangeWindow('win_progressbar');
		changeWindow({id: 'win_save', css: {width: '300px', height: '200px'}});
	}
}