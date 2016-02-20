window.alert = romanya.createMessageTitledWindow;

function toggleVisibility(id){
	e = jQuery(id);
	if (e.is(':hidden')){
		e.fadeIn("slow");
		e.find(":input").removeAttr('disabled');
	}else{
		e.fadeOut("slow");
		e.find(":input").attr("disabled", true);
	}
}

function CreateBookmarkLink() 
{
	var title = "okotown.ru";
	var url = document.location;
	if (window.sidebar)
	{
		// Mozilla Firefox Bookmark
		window.sidebar.addPanel(title, url,"");
	}
	else if( window.external && window.navigator.userAgent.indexOf ("MSIE") >= 0)
	{
		// IE Favorite
		window.external.AddFavorite( url, title);
	}
	else alert('Для добавления закладки нажмите Ctrl+D');
}

function flashVersion() {
   // Отдельно определяем Internet Explorer
   var ua = navigator.userAgent.toLowerCase();
   var isIE = (ua.indexOf("msie") != -1 && ua.indexOf("opera") == -1 && ua.indexOf("webtv") == -1);
   // Стартовые переменные
   var version = 0;
   var lastVersion = 20; // c запасом
   var i;

   if (isIE) { // browser == IE
	  try {
		 for (i = 3; i <= lastVersion; i++) {
			if (eval('new ActiveXObject("ShockwaveFlash.ShockwaveFlash.'+i+'")')) {
			   version = i;
			}
		 }
	  } catch(e) {}
   } 

   else { // browser != IE
	  for (i = 0; i < navigator.plugins.length; i++) {
		 if (navigator.plugins[i].name.indexOf('Flash') != -1) {
			var strLength = navigator.plugins[i].description.length;
			version = parseFloat(navigator.plugins[i].description.substring(15, navigator.plugins[i].description.indexOf('r')));					
		 }
	  }
   }

   if (version >= 10) {
	  return true;
   } else {
	  return false;
   }

}

function messageFlash(size)
{
	document.write('<div style="width: '+ size.w +'; height: '+ size.h +';" class="noFlash">');
	document.write('У вас отсутствует или установлена старая версия flash плеера. Новую версию плеера можно скачать <a target="_blank" href="http://get.adobe.com/flashplayer/">тут</a>');
	document.write('</div>');
}
