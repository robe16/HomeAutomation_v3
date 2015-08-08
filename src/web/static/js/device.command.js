function sendCommand(cmd) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", cmd, false);
        xmlHttp.send(null);
        var v = document.getElementById('alert')
        if (xmlHttp.responseText=200){
            v.innerHTML = "The command has been successfully sent";
            v.setAttribute('class', 'alert alert-success');
        } else {
            v.innerHTML = "<strong>Error!!</strong> The command has not been successful being sent to the device";
            v.setAttribute('class', 'alert alert-danger');
        }
        v.style.visibility="visible";
        setTimeout(function(){v.style.visibility="hidden"}, 2000);
    }