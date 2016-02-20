// инициализация
function init() {
    initTooltip();
    initMenuFilter();
}
// инициализация всплыв подсказок
function initTooltip() {
    $(".short_descr").easyTooltip();
}
// инициализация меню фильтра
function initMenuFilter() {
    $("#menu_filters li a").click(function() {
        $("#menu_filters li").removeClass("mcf_act");
        $(this).parent().addClass("mcf_act");
        var status = $(this).attr("id").split("_")[1];
        var block = $("#block_" + status);
        $(".list_result_learn").hide();
        block.slideDown("normal");
        return false;
    });
}