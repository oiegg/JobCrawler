$.ready(init());

function init(){
    load_post_list();
    load_recent_post();
}

function load_post_list(){
    $.getJSON("/inspector/status/1", function(data){
        var li = $("#post ul");
        li.empty();
        $.each(data['info'], function(key, val){
            li.append($("<li/>", {
                class: "list-group-item",
                html: "<a href=\"" + val["source_url"] + "\">" + val["title"] + "</a>"
            }));
        });
        $("#post ul li").each(function(){
            $(this).click(function(){
                load_info($(this).find("a").attr("href"));
            });
        });
        if (data) load_info();
    });
}

function load_recent_post(){
    $.getJSON("/inspector/status/2", function(data){
        var li = $("#recent_post ul");
        li.empty();
        $.each(data['info'], function(key, val){
            li.append($("<li/>", {
                class: "list-group-item",
                html: "<a href=\"" + val["post_url"] + "\">" + val["title"] + "</a>"
            }));
        });
    });
}

function load_info(url){
    if (!url){
        url = $("#post a:first").attr("href");
    }
    $.getJSON('/inspector/info?source_url=' + url, function(data){

    });
}

function feedme(){
    $.getJSON('/crawler/update', function(data){
        load_post_list();
        load_info();
    });
}