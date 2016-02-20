var DEFAULT_WIDTH = '300px';
var DEFAULT_HEIGHT = '200px';
// функции для окон
function screenSize2() {
	return { width: $(window).width(), height: $(window).height() }
}
function getBodyScrollTop2() {
	return $(window).scrollTop();
}
function positionScreen2(param) {
	var elem = param.obj;
	var pos_elem = elem.offset();
	var top = pos_elem.top - param.distY; //+ getBodyScrollTop2();
	var left = pos_elem.left + elem.width() + param.distX;
	var scr = screenSize2();
	if ( ( left + param.win_width ) > scr.width ) {
		left = pos_elem.left - param.win_width - param.distX;
	}
	if (param.win_height) {
		if ( ( top + param.win_height ) > scr.height ) {
			top = scr.height - param.win_height - param.distY;
		}
	}
	return { top: top, left: left };
}
function closeWindow2(id) {
	$("#" + id).hide();
	$("#block_fon").hide();
}
function removeEvent2(obj, e) {
	obj.unbind(e);
}
// закрытие окна на esc
function closeWindowOnEsc(e, cls, f) {
	var code = e.keyCode;
	if ( code == 27 ) {
		if (cls) {
			var wins = $("body").find("." + cls)
		} else {
			var wins = $("body").find(".winFloating")
		}
		$.each(wins, function() {
			if ($(this).css("display") == "block") {
				closeWindow2($(this).attr("id"));
				if (f) f.call();
			}
		});
	}
}
// создание диалогового окна
function changeWindow2(param) {
	var win = $("#" + param.id);
	win.css("width", DEFAULT_WIDTH);
	win.css("height", DEFAULT_HEIGHT);
	var content = win.find("div.contWF");
	if (param.head) {
		win.find("div.headWF_txt").html(param.head);
	}
	if (param.txt) {
		content.html(param.txt);
	}
	if (param.css) {
		for (var i in param.css) {
			win.css(i, param.css[i])
		}
	}
	content.css("height", win.height() - 62 + 'px');
	var scr = screenSize2();	
	var t = (scr.height - parseInt(win.css("height")))/ 2*0.8;
	if (t < 0) { t = 0 }
	t = t + 'px';
	win.css("top", t);
	win.css("left", (scr.width - parseInt(win.css("width"))) / 2 + 'px');
	var fon = $("#block_fon");	
	if ($.browser.msie && $.browser.version == "6.0") {
		win.css("top", parseInt(t)+ document.documentElement.scrollTop +'px')
		fon.css("height", document.body.offsetHeight + 'px');
	}
	if (param.css) {
		if (param.css.top && param.css.left) {
			 win.css("top", param.css.top);
			 win.css("left", param.css.left);
		} 
	}   
	if (param.noblock) {
		fon.hide();
	} else {
		fon.show();
	}	
	win.show();
	var btn_cancel = win.find("div.bodyWF div.footerWF .close")
	var btn_close = win.find("div.bodyWF div.btnCloseWF input[type=button]");
	removeEvent2(btn_close, 'click');
	removeEvent2(btn_cancel, 'click');	
	btn_close.click(function() {
		closeWindow2(param.id);
	});
	btn_cancel.click(function() {
		closeWindow2(param.id);	
	});	
}
// создание информационного окна
function createInfoWindow2(param) {
	var distX = param.distX ? param.distX : 0; 
	var distY = param.distY ? param.distY : 0; 
	var w1 = param.width;
	var h1 = param.height;
	var win = $("#" + param.id);
	var content = win.find("div.contWF_add");
	if (param.txt) {
		content.html(param.txt);
	}
	content.parent().css("height", h1 - 62 + 'px');
	var fon = $("#block_fon");

	var pos_win = positionScreen2({obj: param.obj, win_width: w1, win_height: h1, distX: distX, distY: distY});
	var coord_left = pos_win.left + "px";
	var coord_top = pos_win.top - 15 + "px";
	win.css("width", w1);
	win.css("height", h1);
	win.css("left", coord_left);
	win.css("top", coord_top);
	if ($.browser.msie && $.browser.version == "6.0") {
		win.css("top", parseInt(coord_top) + getBodyScrollTop2() +'px')
		fon.css("height", document.body.offsetHeight + 'px');
	}
	fon.show();
	win.show();
}
// индикатор загрузки
function showIndicator(show) {
	var win = $("#indicator");
	var fon = $("#block_fon");
	if (show) {
		var w = 300;
		var h = 100;
		var scr = screenSize2();
		var t = (scr.height - parseInt(win.css("height")))/ 2*0.8;
		win.css("top", t + "px");
		win.css("left", (scr.width - parseInt(win.css("width"))) / 2 + 'px');
		if ($.browser.msie && $.browser.version == "6.0") {
			win.css("top", parseInt(t)+ document.documentElement.scrollTop +'px')
			fon.css("height", document.body.offsetHeight + 'px');
		}
		fon.show();
		win.show();
	} else {
		win.hide();
		fon.hide();		
	}
}

function createTitleWindow(param) {
	var distX = param.distX ? param.distX : 0; 
	var distY = param.distY ? param.distY : 0; 
	var win = $("#" + param.id);   
	var pos_win = positionScreen2({obj: param.obj, win_width: parseInt(win.css("max-width")), win_height: parseInt(win.css("max-height")), distX: distX, distY: distY});
	var coord_left = pos_win.left + "px";
	var coord_top = pos_win.top + "px";
	win.css("left", coord_left);
	win.css("top", coord_top);
	win.show();
}
// windowJournal({id: 'win_journal', css: {width: '600px', height: '600px'}, txt:"bbbbb", pos: '1'});
function windowJournal(param) {
	var border_left = 20;
	var border_top = 20;
	var scroll_width = 16;
	var dist_ie6 = 10;
	var win = $("#" + param.id);
	var fon = $("#block_fon"); 
	if (param.css) {
		for (var i in param.css) {
			win.css(i, param.css[i])
		}
	}
	if (param.head) {
		win.find("div.headWF_txt").html(param.head);
	} 
	var content = win.find("div.contWF_add");
	if (param.txt) {
		content.html(param.txt);
	}
	content.parent().css("height", win.height() - 32 + 'px');
	var scr = screenSize2();
	if (param.pos == 0) {
		var t = (scr.height - win.height()) / 2 * 0.8;
		if (t < 0) { t = 0 }
		t = t + 'px';
		win.css("top", t);
		win.css("left", (scr.width - win.width()) / 2 + 'px');
		if ($.browser.msie && (($.browser.version == "6.0") || ($.browser.version == "7.0"))) {
			win.css("position", "absolute");
			win.css("top", parseInt(t)+ document.documentElement.scrollTop +'px')
			fon.css("height", document.body.offsetHeight + 'px');			
		} else {
			win.css("position", "fixed")
		}	
	} else {
		var t = scr.height - win.height() - border_top;
		if (t < 0) { t = 0 }
		t = t + 'px';
		win.css("top", t);
		win.css("right", '5px');
		if ($.browser.msie && (($.browser.version == "6.0") || ($.browser.version == "7.0"))) {
			win.css("position", "absolute");
			win.css("top", parseInt(t)+ document.documentElement.scrollTop - dist_ie6 +'px');
			fon.css("height", document.body.offsetHeight + 'px');
		} else {
			win.css("position", "fixed")
		}
	}
	win.show();
	fon.show();	
}