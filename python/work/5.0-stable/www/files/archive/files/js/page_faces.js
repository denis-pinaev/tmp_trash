function initFacesSize(){
    var sizes = $(".block_photo img");
    $.each(sizes, function(key, value) {
		var element = $(this);
		size_str = element.width()+"x"+element.height();
		if (size_str != "x") {
		    $("#span_"+element.attr("id")).html(size_str);
		}							
	});
}