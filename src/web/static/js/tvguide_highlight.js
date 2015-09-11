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

function getChannel(url, auto) {
    //
    response = sendHttp(url, null, 'GET', true, false);
    if (response) {channelhighlight('chan'+response)}
    //
    if (auto) {setTimeout(function () {getChannel(url);}, 10000);}
    //
}