function sendCommand(cmd) {

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", cmd, false);
    xmlHttp.send(null);

    if (xmlHttp.responseText=200){
        document.getElementById("alert").innerHTML = "The command has been successfully sent";
        document.getElementById("alert").style["display"] = "inline";
        document.getElementById("alert").className = "alert alert-success";
        (document.getElementById("alert").style["display"] = "none").delay(3000);
    } else {
        document.getElementById("alert").innerHTML = "<strong>Error!!</strong> The command has not been successful being sent to the device";
        document.getElementById("alert").style["display"] = "inline";
        document.getElementById("alert").className = "alert alert-danger";
        (document.getElementById("alert").style["display"] = "none").delay(3000);
    }
}