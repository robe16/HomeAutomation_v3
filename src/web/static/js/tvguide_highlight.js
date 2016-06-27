function channelhighlight(channo) {
    var all = document.getElementsByTagName("div");
    for (var i = 0; i < all.length; i++)
        {
            if (all[i].id==(channo)) {
                document.getElementById(all[i].id).classList.add("chan-highlight");
            }
            else if (all[i].id.startsWith('chan')) {
                document.getElementById(all[i].id).classList.remove("chan-highlight");
            };
        };
}

function getChannel(url, auto) {
    //
    response = sendHttp(url, null, 'GET', 1, false);
    if (response) {channelhighlight('chan'+response)}
    //
    if (auto) {setTimeout(function () {getChannel(url);}, 10000);}
    //
}