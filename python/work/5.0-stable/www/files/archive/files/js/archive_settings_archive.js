var params = new Array(); // массив значений, формируется при загрузке страницы
// применение настроек
function applyChanges() {
	var options = {
		method: "POST",	  
		url: "/archive/command/set_daemon_settings/",	  
		data: {id: $("#archive_sel").attr("value")},
		success: function(obj) {
			if (obj && obj.status) {
			showMessage(MESSAGE["4"]);
			} else {
			showMessage('<span class="error">' + ERROR["10"] + '</span>');
			}
		},
		error: function(msg) {
			showMessage('<span class="error">' + ERROR["10"] + '</span>');  
		}
	};
	$("#ArchiveForm").ajaxSubmit(options);
}
// сброс настроек
function resetChanges(){
	var validator = $("#ArchiveForm").validate();
	validator.resetForm();
}
// окно удаления видеоархива
function deleteArchive() {
	changeWindow({id: 'win_del', css: {width: '300px', height: '200px'}, txt: MESSAGE["1"]});
}
// удаление видеоархива
function delArchive(){
	var options = {
	  method: "POST",	  
	  url: URL[0],	  
	  data: {id: $("#archive_sel").attr("value")},
	  success: function(obj) {
	      closeChangeWindow('win_del');	  
	      var msg = eval("("+obj+")");
	      if (msg.status){      
	          //showMessage(MESSAGE[3]);
			  location.href = URL[2];
	      }else{
	          showMessage(ERROR[6]);
	      }
	  },
	  error: function(msg) {
	    closeChangeWindow('win_del');
		showMessage(ERROR[6]);
	  }
	};
	$("#frmAddArchive").ajaxSubmit(options);    
}
// окно добавления видеоархива
function addArchive() {
	changeWindow({id: 'win_add', css: {width: '320px', height: '240px'}});
}
// проверка формы добавления видеоархива
function checkFormAddArchive() {
	var validator = $("#frmAddArchive").validate({
		rules: {
			ip: {
				required: true
			},
			url: {
				required: true		
			}
		},
		messages: {
			ip: {
				required: ERROR[9]
			},			
			url: {
				required: ERROR[7]
			}		
		},
		errorPlacement: function(error, element) {
			error.appendTo( element.parent().prev() ); 
		},
		submitHandler: function() {	
			closeChangeWindow('win_add');
			addNewArchive();
		}
	});
}
// добавление видеоархива
function addNewArchive(){
	var options = {
		method: "POST",	  
		url: URL[1],	  
		data: {id: $("#archive_sel").attr("value")},
		success: function(obj) {
			closeChangeWindow('win_add');
			var msg = eval("("+obj+")");
			if (msg.status){     
				showMessage(MESSAGE[2]);	                       
				if (msg.error.length > 0) $('#archive_list').html(msg.error);
			} else {
				if (msg.error == "dublicate") {
					showMessage(ERROR[5]);
				} else {
					showMessage(ERROR[4]);
				}
			}
		},
		error: function(msg) {
			closeChangeWindow('win_add');
			showMessage(ERROR[4]);
		}
	};
	$("#frmAddArchive").ajaxSubmit(options);    
}