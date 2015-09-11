function sendHttp(url, data, getpost, responserequired, alert) {
    var v = document.getElementById('alert')
    try {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open(getpost, url, false);
        xmlHttp.send(data);
        if (alert){
            if (xmlHttp.status==200){
                v.innerHTML = "The command has been successfully sent";
                v.setAttribute('class', 'alert alert-success');
            } else {
                v.innerHTML = "<strong>Error!!</strong> The command has not been successful being sent to the device";
                v.setAttribute('class', 'alert alert-danger');
            }
        }
        v.style.visibility="visible";
        setTimeout(function(){v.style.visibility="hidden"}, 2000);
        if (responserequired) {
            if (xmlHttp.status==200) {return xmlHttp.responseText;} else {return false;}
        }
    }
    catch(err) {
        v.innerHTML = "<strong>Error!!</strong> The command has not been successful being sent to the device";
        v.setAttribute('class', 'alert alert-danger');
        v.style.visibility="visible";
        setTimeout(function(){v.style.visibility="hidden"}, 2000);
        if (responserequired) {return false;}
    }
}