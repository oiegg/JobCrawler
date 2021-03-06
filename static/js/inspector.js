$.ready(init());

function init(){
    load_recent_posted();
    load_recent_crawled();
    load_recent_retry();
    load_recent_garbled();
    load_recent_unknown();
}

function load_recent_posted(){
    $.getJSON('/inspector/status/2', function(data){
        var li = [];
        $.each(data["info"], function(key, val){
            li.push("<li>" + "<a href=\"" + val["post_url"] + "\">" + val["title"] + "</a>" + "</li>");
        });
        var d = $("#recent_posted");
        d.append("<h2>Recent Posted(" + data["total"] + " in total)</h2>");
        d.append($( "<ul/>", {
            html: li.join( "" )
        }));
    });
}

function load_recent_crawled(){
    $.getJSON('/inspector/status/1', function(data){
        var li = [];
        $.each(data["info"], function(key, val){
            li.push("<li>" + "<a href=\"" + val["source_url"] + "\">" + val["title"] + "</a>" + "</li>");
        });
        var d = $("#recent_crawled");
        d.append("<h2>Recent Crawled(" + data["total"] + " in total)</h2>");
        d.append($( "<ul/>", {
            html: li.join( "" )
        }));
    });
}

function load_recent_retry(){
    $.getJSON('/inspector/status/3', function(data){
        var li = [];
        $.each(data["info"], function(key, val){
            li.push("<li>" + "<a href=\"" + val["source_url"] + "\">" + val["title"] + "</a>" + "</li>");
        });
        var d = $("#recent_retry");
        d.append("<h2>Recent Max Retry Exceeded(" + data["total"] + " in total)</h2>");
        d.append($( "<ul/>", {
            html: li.join( "" )
        }));
    });
}

function load_recent_garbled(){
    $.getJSON('/inspector/status/5', function(data){
        var li = [];
        $.each(data["info"], function(key, val){
            li.push("<li>" + "<a href=\"" + val["source_url"] + "\">" + val["title"] + "</a>" + "</li>");
        });
        var d = $("#recent_garbled");
        d.append("<h2>Recent Marked as Garble(" + data["total"] + " in total)</h2>");
        d.append($( "<ul/>", {
            html: li.join( "" )
        }));
    });
}

function load_recent_unknown(){
    $.getJSON('/inspector/status/4', function(data){
        var li = [];
        $.each(data["info"], function(key, val){
            li.push("<li>" + "<a href=\"" + val["source_url"] + "\">" + val["title"] + "</a>" + "</li>");
        });
        var d = $("#recent_unknown");
        d.append("<h2>Recent Failed for Unknown Reasons(" + data["total"] + " in total)</h2>");
        d.append($( "<ul/>", {
            html: li.join( "" )
        }));
    });
}