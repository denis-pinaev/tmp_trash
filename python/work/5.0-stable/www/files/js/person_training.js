function startLearn() {
	$("#block_message_start").slideUp("normal");
	$("#block_message_stop").slideDown("normal");
	$("#block_message_faces").hide();
	$("#list_faces").show();
}
function errorMessage(show, txt) {
	var block = $("#block_error");
	if (txt) {
		var msg = txt;
		block.html(msg)
	}
	if (show) {
		block.slideDown("normal");
		$("html").scrollTop(0);	
	} else {
		block.slideUp("normal");
	}
}