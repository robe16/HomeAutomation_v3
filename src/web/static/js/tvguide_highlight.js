function channelhighlight(channo) {
    var all = document.getElementsByTagName("tr");
    for (var i = 0; i < all.length; i++)
        {
            if (all[i].id==(channo)) {
                document.getElementById(all[i].id).className="highlight";
            }
            else if (all[i].id.startsWith('chan')) {
                document.getElementById(all[i].id).className="";
            };
        };
}

function getChannel(cmd) {
    //
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", cmd, false);
    xmlHttp.send(null);
    if (xmlHttp.status==200) {
        channelhighlight('chan'+(xmlHttp.responseText))
    }
    //
}