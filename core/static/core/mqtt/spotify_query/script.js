var url = window.location.href;
var match = url.match(/tmpClient_(\d+)/);
if (match) {
    var tmpClientUser = 'tmpClient_'+ match[1];
} else {
    var tmpClientUser = 'tmpClient_'+ Math.round(Math.random() * (0-10000) * -1);
}

$(document).ready(function filterAutoSet() {
    var get_url = window.location.href;
    if (get_url.match(/track/)) {
        $("#track_id").attr('class', 'nav-link active');
    } else if (get_url.match(/album/)) {
        $("#album_id").attr('class', 'nav-link active');
    } else if (get_url.match(/artist/)) {
        $("#artist_id").attr('class', 'nav-link active');
    } else if (get_url.match(/playlist/)) {
        $("#playlist_id").attr('class', 'nav-link active');
    } else {
        $("#track_id").attr('class', 'nav-link active');
    }
});

function filterCheck(filter_id){
    var count;
    var class_selection = $("#"+filter_id).attr('class').split(" ");
    
    for (count = 0; count < class_selection.length; count++) {
        if (class_selection[count] == "active") {
            return true;
        }
    }
    return false;
}

function buildQueryToLink(anchor_id) {
    var filter_selected;
    if (filterCheck("track_id")) {
        filter_selected="track";
    } else {
        if (filterCheck("album_id")) {
            filter_selected="album";
        } else {
            if (filterCheck("artist_id")) {
                filter_selected="artist";
            } else {
                if (filterCheck("playlist_id")) {
                    filter_selected="playlist";
                } else {
                    filter_selected="track";
                }
            }
        }
    }
    var input_keyword_query = document.getElementById("keyword_query_id");
    var keyword_query = input_keyword_query.value;
    var new_url="?filter="+filter_selected+"&q="+keyword_query+"&"+tmpClientUser;
    var spotify_anchor = document.getElementById(anchor_id);
    spotify_anchor.href = spotify_anchor.href + new_url;
}