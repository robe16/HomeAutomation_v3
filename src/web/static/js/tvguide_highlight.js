function channelhighlight(channo) {
    var all = document.getElementsByTagName("a");
    for (var x of all)
        if (all[x].id=(channo)) {
            document.getElementById(all[x]).setAttribute('border', '#FFBF47');
            document.getElementById(all[x]).setAttribute('border-radius', '7px');
        }
        else if (all[x].id.startsWith('chan')) {
            document.getElementById(all[x]).style.removeProperty('border');
            document.getElementById(all[x]).style.removeProperty('border-radius');
        };
}