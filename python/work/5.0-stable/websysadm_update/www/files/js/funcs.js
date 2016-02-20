function byId(v){
    return document.getElementById(v)
}

function screenSize() {
    var w = '';
    var h = '';
    w = (window.innerWidth ? window.innerWidth : (document.documentElement.clientWidth ? document.documentElement.clientWidth : document.body.offsetWidth));
    h = (window.innerHeight ? window.innerHeight : (document.documentElement.clientHeight ? document.documentElement.clientHeight : document.body.offsetHeight));
    return { w: w, h: h };
}

function showIndicator(show) {
    var win = byId('indicator');
    var fon = byId('block_fon');
    if (show) {
        var w = 200;
        var h = 60;
        var scr = screenSize();
        win.style.top = (100 - h*100/scr.h)/3/100*scr.h + 'px';
        win.style.left = (scr.w - w) / 2 + 'px';
        fon.style.display = 'block';
        win.style.display = 'block';
    } else {
        fon.style.display = 'none';
        win.style.display = 'none';
    }
}

function export_info(){
    showIndicator(true);
    fr = 0;
    if (document.getElementById("fr")){
        if (document.getElementById("fr").checked){fr = 1;}                                       
    }
    journal = 0;
    if (document.getElementById("journal")){
        if (document.getElementById("journal").checked){journal = 1;}                                       
    }    
    admin = 0;
    if (document.getElementById("admin")){
        if (document.getElementById("admin").checked){admin = 1;}                                       
    }    
    db = 0;
    if (document.getElementById("db")){
        if (document.getElementById("db").checked){db = 1;}                                       
    }    
    version = 0;
    if (document.getElementById("version")){
        if (document.getElementById("version").checked){version = 1;}                                       
    }    
    document.getElementById("div_info").innerHTML = "";
    $.ajax({
        type: "GET",
        url: "/exportinfo",
        data: {version: version, db: db, admin: admin, journal: journal, fr: fr},
        success: function(msg){
//            alert(msg);
            var content = '<ul class="list_links">'+msg+'</ul>';
            document.getElementById("div_info").innerHTML = content;
            showIndicator(false);
        },
        error: function(msg){
  //          alert("!!!"+msg);
            showIndicator(false);
        }        
    });        
}

function reboot_system(){
    showIndicator(true);
    $.ajax({
        type: "GET",
        url: "/rebootsystem",
        data: {},
        success: function(msg){
            showIndicator(false);
        },
        error: function(msg){
            showIndicator(false);
        }        
    });        
}
