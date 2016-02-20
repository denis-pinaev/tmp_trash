(function($) {

	$.fn.easyTooltip = function(options){
	  
		// default configuration properties
		var defaults = {	
			xOffset: 10,		
			yOffset: -10,
			tooltipId: "easyTooltip",
			clickRemove: false,
			content: "",
			useElement: ""
		}; 
			
		var options = $.extend(defaults, options);  
		var content;
		var cursorWidth = 5;
				
		this.each(function() {  				
			var title = $(this).attr("title");				
			$(this).hover(function(e){											 							   
				content = (options.content != "") ? options.content : title;
				content = (options.useElement != "") ? $("#" + options.useElement).html() : content;
				$(this).attr("title","");
				if (content != "" && content != undefined){
					if (document.getElementById(options.tooltipId) == null) {
						$("body").append("<div id='"+ options.tooltipId +"'>"+ content +"</div>");
					}
					if ($(document).width() / 2 < e.pageX) {
						$("#" + options.tooltipId)
							.css("top",(e.pageY - options.yOffset) + "px")
							.css("left",(e.pageX - $("#" + options.tooltipId).width() - options.xOffset - cursorWidth) + "px")						
							.fadeIn("slow")
					} else {
						$("#" + options.tooltipId)
							.css("top",(e.pageY - options.yOffset) + "px")
							.css("left",(e.pageX + options.xOffset) + "px")
							.fadeIn("slow")					
					}
				}
			},
			function(){
				$("#" + options.tooltipId).remove();
				$(this).attr("title",title);
			});	
			$(this).mousemove(function(e){
				if ($(document).width() / 2 < e.pageX) {
					$("#" + options.tooltipId)
							.css("top",(e.pageY - options.yOffset) + "px")
							.css("left",(e.pageX - $("#" + options.tooltipId).width() - options.xOffset - cursorWidth) + "px")				
				} else {
					$("#" + options.tooltipId)
						.css("top",(e.pageY - options.yOffset) + "px")
						.css("left",(e.pageX + options.xOffset) + "px")
				}
			});	
			if(options.clickRemove){
				$(this).mousedown(function(e){
					$("#" + options.tooltipId).remove();
					$(this).attr("title",title);
				});				
			}
		});
	  
	};
})(jQuery);