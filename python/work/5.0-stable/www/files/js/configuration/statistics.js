var processing = {}; // массив из процессов
var TOOLTIP_DIST_LEFT_BAR = 30;
var TOOLTIP_DIST_LEFT_LINE = 10;

var datasets_daemon = [];
var datasets_traffic = [];
var datasets_daemon_time = [];
var datasets_faces = [];

function init() {
    $(".list_period li a").click(function() {
        getInfoStatistics($(this));
        return false;
    });
    $("#period_info").html(getCurrentDate("."));
    setDateSever(getCurrentDate("."), getCurrentDate("."), "daemons_chart_by_day");
    getStatistic('daemon');
    getStatistic('traffic');
    getStatistic('daemon_time');
    getStatistic('faces');
    getTableStatistic();
    checkChooseLinerGraph();
    $(".type_graphs li input").click(function(e) {
        chooseLinerGraph($(this));
    });
}
// получить информацию по статистике
function getInfoStatistics(obj) {
    showPeriod(obj);
    setPeriod(obj);                              
}
// получить текущую дату
function getCurrentDate(delim, delim_server) {
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
function getFormatDateAxisX(date, delim) {
    var day = ((String(date.getDate()).length == 1)) ? "0" + date.getDate() : date.getDate();
    var month = ((String(date.getMonth()+1).length == 1)) ? "0" + (date.getMonth() + 1) : (date.getMonth() + 1);
    return (day + delim + month);                        
}

// функции для выбора типа линий
// проверка какой тип линии выбран
function checkChooseLinerGraph() {
    var type_graphs = $(".type_graphs");
    $.each(type_graphs, function() {
        var name_graph = $(this).attr("id").split("_type_graphs")["0"];
        var type_liner = $("#" + name_graph + "_type_graphs_cur").val();
        $(this).find("li").removeClass("tg_act");
        var btns = $(this).find("li input");
        $.each(btns, function() {
            var cls = "graph_" + type_liner;
            if ($(this).attr("class") == cls) {
                $(this).parent().addClass("tg_act");
            }
        });
        setLeftAxisY(name_graph);    
    });    
}
// установить левую коорд-ту названия оси по Y
function setLeftAxisY(name_graph) {
    var axisY = $("#" + name_graph + "_axisY");
    var axisY_left = $("#" + name_graph + "_graph div.tickLabels div.tickLabel:last").width();
    axisY.css("left", axisY_left + 3 + "px");
}
// установить названия оси по X
function setAxisX(name, query) {
    var axisX = $("#" + query + "_axisX");    
    switch (name) {
        case "daemons_chart_by_day_yesterday":
            axisX.html(textHours);
            break;
        case "daemons_chart_by_day":
            axisX.html(textHours);
            break;
        case "daemons_chart_by_week":
            axisX.html(textDays);
            break;
        case "daemons_chart_30days":
            axisX.html(textDays);
            break;            
        default:            
            break;
    }

}
// выбор типа линии для графика
function chooseLinerGraph(obj) {
    var name_graph = getNameGraph(obj);
    var type_liner = getTypeLinerGraph(obj, name_graph);
    var datasets = getDatasets(name_graph);
    drawGraph(name_graph, type_liner, datasets);
    activeTypeLinerGraph(obj, name_graph);
    setLeftAxisY(name_graph);
}
// получить название текущего графика
function getNameGraph(obj) {
    var block = obj.parent().parent();
    var block_id = block.attr("id");
    var type = block_id.split("_type_graphs")["0"];
    return type;
}
// получить тип линий для графика
function getTypeLinerGraph(obj, name_graph) {
    var type_liner = obj.attr("class").split("graph_")[1];
    $("#" + name_graph + "_type_graphs_cur").val(type_liner);
    return type_liner;
}
// получить данные для текущего графика
function getDatasets(name_graph) {
    switch (name_graph) {
        case "daemon": {
            return datasets_daemon;
            break;
        }
        case "traffic": {
            return datasets_traffic;
            break;
        }
        case "daemon_time": {
            return datasets_daemon_time;
            break;
        }
        case "faces": {
            return datasets_faces;
            break;
        }
    }
}
// установить данные для текущего графика
function setDatasets(name_graph, datasets) {
    switch (name_graph) {
        case "daemon": {
            datasets_daemon = datasets;
            break;
        }
        case "traffic": {
            datasets_traffic = datasets;
            break;
        }
        case "daemon_time": {
            datasets_daemon_time = datasets;
            break;
        }
        case "faces": {
            datasets_faces = datasets;
            break;
        }
    }
}
// выделение активного типа линий
function activeTypeLinerGraph(obj, name_graph) {
    $("#" + name_graph + "_type_graphs li").removeClass("tg_act");
    obj.parent().addClass("tg_act");
}
// установить параметры для сервера
function setDateSever(date_beg, date_end, name) {
    var delim = "-";
    var date_beg = parseDate(date_beg, ".");
    var date_end = parseDate(date_end, ".");
    var period = date_beg.year + delim + date_beg.month + delim + date_beg.day + ";" + date_end.year + delim + date_end.month + delim + date_end.day + ";" + name;
    $("#period_info_server").val(period);
}
// показать период
function showPeriod(obj) {
    var periods = $(".list_period li");
    $.each(periods, function(key, value) {
        $(this).removeClass("lp_active");
    });
    obj.parent().addClass("lp_active");
}
// скрыть все блоки навигации
function hideBlocksNav() {
    var blocks_nav = $(".block_filter").children("div.nav");
    $.each(blocks_nav, function(key, value) {
        $(this).hide();
    });
}
// установить период
function setPeriod(obj) {
    var period_name = obj.attr("id").split("link_")[1];
    var period = getPeriod(period_name, ".");

    $("#period_info").html(period.date);
    $("#period_head").html(period.head);

    getStatistic('daemon');
    getStatistic('traffic');
    getStatistic('daemon_time');
    getStatistic('faces');
    getTableStatistic();
}
// получить дату/период
function getPeriod(name, delim) {
    var date = new Date();
    var period_date = "";
    var period_head = "";
    switch (name) {
        case "daemons_chart_by_day_yesterday":
            date.setDate(date.getDate() - 1);
            period_date = getFormatDate(date, delim);
            period_head = "Дата";
            setDateSever(period_date, period_date, name);
            break;
        case "daemons_chart_by_week":
            var date_end = getFormatDate(date, delim);
            date.setDate(date.getDate() - 6);
            var date_beg = getFormatDate(date, delim);
            period_date = date_beg + " - " + date_end;
            period_head = "Период";
            setDateSever(date_beg, date_end, name);
            break;
        case "daemons_chart_30days":
            var date_end = getFormatDate(date, delim);
            date.setDate(date.getDate() - 29);
            var date_beg = getFormatDate(date, delim);
            period_date = date_beg + " - " + date_end;
            period_head = "Период";
            setDateSever(date_beg, date_end, name);
            break;
        case "daemons_chart_by_month":
            var date_end = getFormatDate(date, delim);
            var date_beg = "01" + delim + parseDate(date_end, delim).month + delim + parseDate(date_end, delim).year;
            period_date = date_beg + " - " + date_end;
            period_head = "Период";
            setDateSever(date_beg, date_end, name);
            break;            
        default:            
            period_date = getFormatDate(date, delim);
            period_head = "Дата";
            setDateSever(period_date, period_date, name);
            break;
    }
    return {date: period_date, head: period_head};                
}
// получить отдельно день-месяц-год
function parseDate(date, delimiter) {
    var array = date.split(delimiter);
    return {day: array[0], month: array[1], year: array[2]};
}
function parseDate2(date, delimiter) {
    var array = date.split(delimiter);
    return {day: array[2], month: array[1], year: array[0]};
}
// показать ошибку
function showError(msg_err, id_block) {
    if (msg_err) {
        $("#" + id_block).html(msg_err);
        $("#" + id_block).show();
    } else {
        $("#" + id_block).hide();
    }
}
// индикатор загрузки 
function showIndicator(show, id_block) {
    if (show) {
        $("#" + id_block).show();
    } else {
        $("#" + id_block).hide();
    }
}
// получить данные для статистики
function getStatistic( query ) {
    var period = $("#period_info_server").val().split(";"); 
    //alert("period ---> " + period + " ---> " + query);   
    $.ajax({
        url: URL_GET_STATISTICS,
        type:'POST',
        dataType: 'json',
        data: 'start_date='+ period[0] + ';end_date=' + period[1] + ';query=' + query + ';user_login=' + USER,
        timeout: 20000,
        beforeSend: function(){
            $("#" + query + "_graph").empty();
            $("#" + query + "_choices").empty();
            showError(false, query + "_error");
            showIndicator(true, query + "_indicator");
            $("#" + query + "_graph").hide();
            $("#" + query + "_graph").next().hide();
            $("#" + query + "_graph").parent().next().hide();
            processing[query] = 'true';
            isProcessing();		
        },
        success: function(msg) {
            var obj = eval(msg);
            if (obj && obj.status){
                var msg_err = "";
                msg_err = ERR[obj.status];
                showIndicator(false, query + "_indicator");
                showError(msg_err, query + "_error");     
            } else if (obj && (obj.result)) {
                showIndicator(false, query + "_indicator");
                showResult(obj.result["resp"], period[2], query);               
            }
            processing[query] = 'false';
            isProcessing();               
        },
        error: function() {
            var msg_err = textErr3;
            showIndicator(false, query + "_indicator");
            showError(msg_err, query + "_error");
            processing[query] = 'false';
            isProcessing();            
        } 
    });
    
}
// Функции для отображения графика
// нарисовать график
function drawGraph(name_graph, type_liner, datasets) {
    var options = null;
    if (type_liner == "bar") {
        options = {
            series: { stack: true, bars: { show: true, lineWidth: 0.5 } },
            xaxis: { tickSize: 1,  tickFormatter: function (v) { return setValueDayAxisX(v); } },
            yaxis: { min: 0 },
            grid: { backgroundColor: { colors: ["#f2f2f2", "#eee"] }, hoverable: true, borderWidth: 1 },
            legend: { noColumns: 3 }        
        }
    } else if (type_liner == "line_points") {
        options = {
            series: { lines: { show: true, lineWidth: 2 }, points: { show: true, radius: 4 } },
            xaxis: { tickSize: 1,  tickFormatter: function (v) { return setValueDayAxisX(v); } },
            yaxis: { min: 0 },
            grid: { backgroundColor: { colors: ["#f2f2f2", "#eee"] }, hoverable: true },
            legend: { noColumns: 3 }        
        }
    } else {
        options = {
            series: { lines: { show: true, lineWidth: 2 } },
            xaxis: { tickSize: 1,  tickFormatter: function (v) { return setValueDayAxisX(v); } },
            yaxis: { min: 0 },
            grid: { backgroundColor: { colors: ["#f2f2f2", "#eee"] }, hoverable: true },
            legend: { noColumns: 3 }        
        }
    }
    $.plot($("#" + name_graph + "_graph"), datasets, options);    
}
// показать график и чекбоксы
function showGraphChoice(datasets, name, query) {    
    var choiceContainer = $("#" + query + "_choices");
    $.each(datasets, function(key, val) {
        choiceContainer.append('<span><input type="checkbox" name="' + key +
                               '" checked="checked" id="id' + key + query + '" class="inp_check" />' +
                               '<label for="id' + key + query + '">' + val.label + '</label></span>');
    });
    choiceContainer.find("input").click(plotAccordingToChoices);
    function plotAccordingToChoices() {
        var data = [];
        var type_liner = $("#" + query + "_type_graphs_cur").val();
        choiceContainer.find("input:checked").each(function () {
            var key = $(this).attr("name");
            if (key && datasets[key])
                data.push(datasets[key]);
        });
        setDatasets(query, data);
        drawGraph(query, type_liner, data);
    }    
    plotAccordingToChoices(datasets, choiceContainer, name);    
}
// Надписи для всплывающих окон
function getTextTooltip(query){
    switch (query) {
        case "daemon": {
            return textTDeamon;
            break;
        }
        case "traffic": {
            return textTTraffic;
            break;
        }
        case "daemon_time": {
            return textTTime;
            break;
        }
        case "faces": {
            return textTFace;
            break;
        }
    }
}
// показать график
function showResult(result, name, query){ 
    $("#" + query + "_graph").show();
    $("#" + query + "_graph").next().show();
    $("#" + query + "_graph").parent().next().show();                                       
    setAxisX(name, query);
    setDatasets(query, eval(result));
    var datasets = getDatasets(query);
    for (var i in datasets) {
        if (datasets[i].label) {
            datasets[i].label = setLegend(datasets[i].label);
            datasets[i].color = setColor(i);
        }
    }
    showGraphChoice(datasets, name, query);    
    var str_tooltip = textQuery;
    if (query == "traffic") {
        str_tooltip = textMb
    } 
    if (query == "daemon_time") {
        str_tooltip = textSec
    }
    if (query == "faces") {
        str_tooltip = textFaces
    }
    var previousPoint = null;
    var previousLabel = null;    
    $("#" + query + "_graph").bind("plothover", function (event, pos, item) {
        if (item) {
            if ((previousPoint != item.dataIndex) || (previousLabel != item.series.label)) {
                previousPoint = item.dataIndex;
                previousLabel = item.series.label;
                $("#tooltip").remove();
                var x = item.datapoint[0].toFixed(2);
                var    y = item.datapoint[1].toFixed(2);
                if ((query == "daemon") || (query == "faces")) {
                    y = parseInt(y);
                }
                var date = new Date();
                date.setDate(date.getDate());
                curr_date = getFormatDate(date, '.');
                value = item.datapoint[item.datapoint.length-1];
                if (item.datapoint.length == 3){
                    value = y - value;
                }                
                if ((name == "daemons_chart_by_day") || (name == "daemons_chart_by_day_yesterday")) {
                    showTooltip(item.pageX, item.pageY,    "<div class='tooltip_time'>" + textPeriod+ ' ' + x + ' ' + textTo + ' ' + ((parseInt(x) + 1)%24 + ".00") + ", "+ curr_date + "</div><div><span class='tooltip_prop'>" +textModule + ":</span> <strong>" + item.series.label + "</strong></div><div><span class='tooltip_prop'>" + getTextTooltip(query) + ": </span> <strong>" + value +  "</strong></div>", query);
                } else {
                    showTooltip(item.pageX, item.pageY,    "<div class='tooltip_time'>"+ ' ' + textPeriod + ' ' + setValueDateTooltip(parseInt(x)) + ' ' + textTo + ' ' + setValueDateTooltip(parseInt(x) + 1) + ", </div><div><span class='tooltip_prop'>" +textModule + ":</span> <strong>" + item.series.label + "</strong></div><div><span class='tooltip_prop'>" + getTextTooltip(query) + ": </span> <strong>" + value +  "</strong></div>", query);
                }
            }
        }
        else {
            $("#tooltip").remove();
            previousPoint = null;
            previousLabel = null;            
        }
    });  
}
// установить названия в легенде
function setLegend(name) {
    var name_new = name;
    switch (name) {
        case "detect":
            name_new = textDetect;
            break;    
        case "detect_and_identification":
            name_new = textIdent;
            break;
        case "fanstudio":
            name_new = textFS;
            break;                            
    }
    return name_new;
}
function setColor(i) {
    var arr_color = ["#FF0000", "#FF9900", "#0000FF"]
    return arr_color[i];
}
// всплывающая подсказка для графика
function showTooltip(x, y, contents, query) {
    var dist_left = getDistLeftTooltip(query);
    $('<div id="tooltip" class="graphTooltip">' + contents + '</div>').css( {
        top: y + 5,
        left: x + dist_left,
        opacity: 0.95
    }).appendTo("body").fadeIn(200);
}
function getDistLeftTooltip(query) {
    var type_liner = $("#" + query + "_type_graphs_cur").val();
    if (type_liner == "bar") {
        return TOOLTIP_DIST_LEFT_BAR;
    } 
    return TOOLTIP_DIST_LEFT_LINE;
}
// установить значения по оси X
// для одного дня
function setValueDayAxisX(v) {
    var value = ((String(v).length == '1')) ? "0" + v : v;
    return value;
}
// для 7 дней
function setValueWeekAxisX(v) {
    var period = $("#period_info_server").val().split(";");
    var date_beg = parseDate2(period[0], "-");
    var date_beg_nf = new Date(date_beg.year, date_beg.month - 1 , date_beg.day);
    var date_cur_nf = new Date(date_beg_nf.setDate(date_beg_nf.getDate() + v));
    var date_cur = getFormatDateAxisX(date_cur_nf, ".");
    var thisDay = date_cur_nf.getDay();
    var weekDays = [textDay7,textDay1,textDay2,textDay3,textDay4,textDay5,textDay6,textDay7];
    thisDay = weekDays[thisDay];
    return date_cur + " (" + thisDay + ")";
}
// для 30 дней
function setValueAxisX(v) {
    var period = $("#period_info_server").val().split(";");
    var date_beg = parseDate2(period[0], "-");
    var date_beg_nf = new Date(date_beg.year, date_beg.month - 1 , date_beg.day);
    var date_cur_nf = new Date(date_beg_nf.setDate(date_beg_nf.getDate() + v));
    var date_cur = getFormatDateAxisX(date_cur_nf, ".");
    return date_cur;
}
// установить значения для тултипа
function setValueDateTooltip(v) {
    var period = $("#period_info_server").val().split(";");
    var date_beg = parseDate2(period[0], "-");
    var date_beg_nf = new Date(date_beg.year, date_beg.month - 1 , date_beg.day);
    var date_cur_nf = new Date(date_beg_nf.setDate(date_beg_nf.getDate() + v));
    var date_cur = getFormatDateAxisX(date_cur_nf, ".");
    return date_cur;
}
// обработка таблицы
// получить статистику по IP
function getTableStatistic( sorto, up ) {
    if (typeof up == "undefined") up = 1;
    if (typeof sorto == "undefined") sorto = 1;  
    var period = $("#period_info_server").val().split(";");
    $.ajax({
        url: URL_GET_TABLE_STATISTICS,
        type:'POST',
        dataType: 'json',
	    data: 'start_date='+ period[0] + ';end_date=' + period[1] + ';query=ip' + ';user_login=' + USER + ';sorto=' + sorto + ';up='+ up,        
        timeout: 20000,
        beforeSend: function(){
            $("#block_table").empty();
            showError(false, "error2");
            showIndicator(true, "indicator2");
            processing['stat'] = 'true';
            isProcessing();                                            
        },
        success: function(msg) {
            obj = eval(msg);                        
            if (obj && obj.status){
                var msg_err = "";
                if (obj.result){
                    msg_err = textErr1 + obj.result;
                } else {
                    msg_err = textErr2;
                }
                showError(msg_err, "error2");     
            } else if (obj && (obj.result)) {                                                        
                $("#block_table").html(obj.result);         
            } 
            showIndicator(false, "indicator2");
            processing['stat'] = 'false';
            isProcessing();            
        },
        error: function() {
            var msg_err = textErr3;
            showIndicator(false, "indicator2");
            showError(msg_err, "error2");
            processing['stat'] = 'false';
            isProcessing();            
        }
    });
    
}
// заблокировать меню, если идёт обработка
function isProcessing() {
    var process = false;
    for (var i in processing) {
        if (processing[i] == "true") {
            process = true;
        }
    }
    if (process) {
        $(".list_period li a").unbind("click");
        $(".list_period li a").addClass("noact");                
    } else {
        $(".list_period li a").click(function() {
            getInfoStatistics($(this));
            return false;
        });                                                    
        $(".list_period li a").removeClass("noact");        
    }
}