var params = new Array();
function init() {
    setCurrentDate();
    $("#periods option:first").attr("selected", "selected");
    $("#periods").change(function() {
        selectPeriod();
    });
    checkForm()
}
// получить текущую дату
function getCurrentDate(delim) {
    var date = new Date();
    return getFormatDate(date, delim);
}
// получить дату в заданном формате
function getFormatDate(date, delim) {
    var day = ((String(date.getDate()).length == 1)) ? "0" + date.getDate() : date.getDate();
    var month = ((String(date.getMonth()+1).length == 1)) ? "0" + (date.getMonth() + 1) : (date.getMonth() + 1);
    var year = date.getFullYear();
    return (day + delim + month + delim + year);                        
}
function setCurrentDate() {
    $("#dataClear").val(getCurrentDate("."));
}
function selectPeriod() {
    var otherPeriod = $("#otherPeriod");
    var selectPeriod = $("#periods option:selected");
    if (selectPeriod.index() == 3) {
        otherPeriod.css("visibility", "visible");
    } else {
        otherPeriod.css("visibility", "hidden");
    }
}
function checkForm() {
    $.validator.addMethod("dateCheck", function(value, element) {
        if ($("#periods option:selected").index() == 3) {
            var date = $(element).val().split(".");
            if (date[0] < 32 && date[0] > 0 && date[1] < 13 && date[1] > 0 && date[2] > 1900) {
                $(element).css("border-color", "#aaaaaa");                                                                               
                return true;
            }
            $(element).css("border-color", "#ff0000");            
            return false;
        }
        $(element).css("border-color", "#aaaaaa");
        return true;
    }, ERROR_DATE );  
    var validator = $("#frm_journal").validate({
        rules: {
            dataClear: {
                dateCheck: true
            }                
        },       
        errorPlacement: function(error, element) {
            error.appendTo( element.parent().parent().parent().prev() ); 
        },
        submitHandler: function() {
            alert("success");
        }  
    });                        
}