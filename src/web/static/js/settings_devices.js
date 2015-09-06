function addRoom(addroomBtnId)
    {
        //
        var roomNum = parseInt(addroomBtnId.substr(addroomBtnId.indexOf("room") + 4))+1;
        //
        //var txtnode = document.createTextNode("Room "+roomNum+":");
        //
        var div = document.createElement("DIV");
        div.setAttribute('id', 'room'+roomNum);
        div.setAttribute('style', "margin-top:10px; margin-bottom:10px");
        //
        var divGrp = document.createElement("DIV");
        divGrp.setAttribute('id', "childdiv-room"+roomNum);
        divGrp.setAttribute('style', "width:90%; float:right;");
        //
        inptroom = createRoomInput(roomNum);
        //
        div.appendChild(inptroom);
        div.appendChild(divGrp);
        //
        document.getElementById('allrooms').appendChild(div);
        //
        document.getElementById(addroomBtnId).setAttribute('id', 'addroom'+roomNum);
        //
    }

function addDevicegroup(roomNum, addgroupBtnId)
    {
        //
        var groupNum = parseInt(addgroupBtnId.substr(addgroupBtnId.indexOf("group") + 5))+1;
        //
        //var txtnode = document.createTextNode("Device group "+groupNum+":");
        //
        var div = document.createElement("DIV");
        div.setAttribute('id', 'room'+roomNum+'group'+groupNum);
        div.setAttribute('style', "margin-top:5px; margin-bottom:5px");
        //
        var divDvcs = document.createElement("DIV");
        divDvcs.setAttribute('id', "childdiv-room"+roomNum+"group"+groupNum);
        divDvcs.setAttribute('style', "width:90%; float:right;");
        //
        inptgroup = createDevicegroupInput(roomNum, groupNum);
        //
        div.appendChild(inptgroup);
        div.appendChild(divDvcs);
        //
        document.getElementById("childdiv-room"+roomNum).appendChild(div);
        //
        document.getElementById(addgroupBtnId).setAttribute('id', 'addroom'+roomNum+'group'+groupNum);
        //
    }

function addDevice(roomNum, groupNum, adddeviceBtnId)
    {
        //
        var deviceNum = parseInt(adddeviceBtnId.substr(adddeviceBtnId.indexOf("device") + 6))+1;
        //
        //var txtnode = document.createTextNode("Device "+deviceNum+":");
        //
        var div = document.createElement("DIV");
        div.setAttribute('id', 'room'+roomNum+'group'+groupNum+'device'+deviceNum);
        div.setAttribute('style', "margin-top:5px; margin-bottom:5px");
        //
        var divDvcProps = document.createElement("DIV");
        divDvcProps.setAttribute('id', "childdiv-room"+roomNum+"group"+groupNum+'device'+deviceNum);
        divDvcProps.setAttribute('style', "width:95%; float:right;");
        //
        inptdevice = createDeviceInput(roomNum, groupNum, deviceNum);
        //
        div.appendChild(inptdevice);
        div.appendChild(divDvcProps);
        //
        document.getElementById("childdiv-room"+roomNum+"group"+groupNum).appendChild(div);
        //
        document.getElementById(adddeviceBtnId).setAttribute('id', 'addroom'+roomNum+'group'+groupNum+'device'+deviceNum);
        //
    }

function changeDevice(id, roomNum, groupNum, deviceNum)
    {
        //
        var childDiv = document.getElementById("childdiv-room"+roomNum+"group"+groupNum+'device'+deviceNum);
        childDiv.innerHTML = ''
        //
        var select = document.getElementById(id);
        var deviceType = select.options[select.selectedIndex].id
        //
        if (deviceType=="lgtv") {
            childDiv.appendChild(createDvcpropsLGTV(deviceType));
        } else if (deviceType=="tivo") {
            childDiv.appendChild(createDvcpropsTIVO(deviceType));
        }
        //
    }

function removeItem(removedivId)
    {
        document.getElementById(removedivId).remove();
    }

function createRoomInput(roomNum)
    {
        //
        ////////////////////////////////
        // Button and glypicon for removing room
        //
        var glyphremove = document.createElement("SPAN");
        glyphremove.setAttribute('class', 'glyphicon glyphicon-remove-sign');
        glyphremove.setAttribute('aria-hidden', 'true');
        //
        var spanremove = document.createElement("SPAN");
        spanremove.setAttribute('class', 'input-group-btn');
        //
        var btnremove = document.createElement("BUTTON");
        btnremove.setAttribute('class', 'btn btn-danger');
        btnremove.setAttribute('button', 'button');
        btnremove.innerHTML = '&nbsp;';
        btnremove.setAttribute('onclick', 'removeItem("room'+roomNum+'")');
        //
        btnremove.appendChild(glyphremove);
        //
        ////////////////////////////////
        // Button for adding device group
        //
        var glyphadd = document.createElement("SPAN");
        glyphadd.setAttribute('class', 'glyphicon glyphicon-plus-sign');
        glyphadd.setAttribute('aria-hidden', 'true');
        //
        var btnadd = document.createElement("BUTTON");
        btnadd.setAttribute('id', 'addroom'+roomNum+'group0');
        btnadd.setAttribute('class', 'btn btn-success');
        btnadd.setAttribute('button', 'button');
        btnadd.innerHTML = '&nbsp;';
        btnadd.setAttribute('onclick', 'addDevicegroup("'+roomNum+'", this.id)');
        //
        var txtnodeadd = document.createTextNode(" Add device group");
        //
        btnadd.appendChild(glyphadd);
        btnadd.appendChild(txtnodeadd);
        //
        ////////////////////////////////
        //
        // Input element for typing room name
        var inputroom = document.createElement("INPUT");
        inputroom.setAttribute('type', 'text');
        inputroom.setAttribute('class', 'form-control');
        inputroom.setAttribute('placeholder', 'Enter room name');
        //
        //
        var inptgrp = document.createElement("DIV");
        inptgrp.setAttribute('class', 'input-group');
        inptgrp.setAttribute('style', 'margin-top: 5px');
        //
        var divbtns = document.createElement("DIV");
        divbtns.setAttribute('class', 'input-group-btn');
        divbtns.appendChild(btnadd);
        divbtns.appendChild(btnremove);
        //
        //
        inptgrp.appendChild(inputroom);
        inptgrp.appendChild(divbtns);
        //
        ////////////////////////////////
        //
        return inptgrp;
        //
        ////////////////////////////////
        //
    }

function createDevicegroupInput(roomNum, groupNum)
    {
        //
        ////////////////////////////////
        // Button and glypicon for removing device group
        //
        var glyphremove = document.createElement("SPAN");
        glyphremove.setAttribute('class', 'glyphicon glyphicon-remove-sign');
        glyphremove.setAttribute('aria-hidden', 'true');
        //
        var spanremove = document.createElement("SPAN");
        spanremove.setAttribute('class', 'input-group-btn');
        //
        var btnremove = document.createElement("BUTTON");
        btnremove.setAttribute('class', 'btn btn-danger');
        btnremove.setAttribute('button', 'button');
        btnremove.innerHTML = '&nbsp;';
        btnremove.setAttribute('onclick', 'removeItem("room'+roomNum+'group'+groupNum+'")');
        //
        btnremove.appendChild(glyphremove);
        //
        ////////////////////////////////
        // Button for adding device
        //
        var glyphadd = document.createElement("SPAN");
        glyphadd.setAttribute('class', 'glyphicon glyphicon-plus-sign');
        glyphadd.setAttribute('aria-hidden', 'true');
        //
        var btnadd = document.createElement("BUTTON");
        btnadd.setAttribute('id', 'addroom'+roomNum+'group'+groupNum+'device0');
        btnadd.setAttribute('class', 'btn btn-success');
        btnadd.setAttribute('button', 'button');
        btnadd.innerHTML = '&nbsp;';
        btnadd.setAttribute('onclick', 'addDevice("'+roomNum+'", "'+groupNum+'", this.id)');
        //
        var txtnodeadd = document.createTextNode(" Add device");
        //
        btnadd.appendChild(glyphadd);
        btnadd.appendChild(txtnodeadd);
        //
        ////////////////////////////////
        //
        // Input element for typing device group name
        var inputdevicegroup = document.createElement("INPUT");
        inputdevicegroup.setAttribute('type', 'text');
        inputdevicegroup.setAttribute('class', 'form-control');
        inputdevicegroup.setAttribute('placeholder', 'Enter device group name');
        //
        //
        var inptgrp = document.createElement("DIV");
        inptgrp.setAttribute('class', 'input-group');
        inptgrp.setAttribute('style', 'margin-top: 5px');
        //
        var divbtns = document.createElement("DIV");
        divbtns.setAttribute('class', 'input-group-btn');
        divbtns.appendChild(btnadd);
        divbtns.appendChild(btnremove);
        //
        //
        inptgrp.appendChild(inputdevicegroup);
        inptgrp.appendChild(divbtns);
        //
        ////////////////////////////////
        //
        return inptgrp;
        //
        ////////////////////////////////
        //
    }

function createDeviceInput(roomNum, groupNum, deviceNum)
    {
        //
        ////////////////////////////////
        // Button and glypicon for removing device
        //
        var glyphremove = document.createElement("SPAN");
        glyphremove.setAttribute('class', 'glyphicon glyphicon-remove-sign');
        glyphremove.setAttribute('aria-hidden', 'true');
        //
        var spanremove = document.createElement("SPAN");
        spanremove.setAttribute('class', 'input-group-btn');
        //
        var btnremove = document.createElement("BUTTON");
        btnremove.setAttribute('class', 'btn btn-danger');
        btnremove.setAttribute('button', 'button');
        btnremove.innerHTML = '&nbsp;';
        btnremove.setAttribute('onclick', 'removeItem("room'+roomNum+'group'+groupNum+'device'+deviceNum+'")')
        //
        btnremove.appendChild(glyphremove);
        //
        ////////////////////////////////
        //
        // Input element for selecting device
        var inputdevice = document.createElement("SELECT");
        inputdevice.setAttribute('id', 'select-room'+roomNum+'group'+groupNum+'device'+deviceNum);
        inputdevice.setAttribute('class', 'form-control');
        inputdevice.setAttribute('onChange', 'changeDevice(this.id, '+roomNum+', '+groupNum+', '+deviceNum+')');
        //
        var options
        var devicesArr = [["-", "-- Please select device --"],["lgtv", "LGTV"],["tivo", "Virgin Media"]]
        //
        for (var i = 0; i < devicesArr.length; i++) {
            options = document.createElement("OPTION")
            options.setAttribute('id', devicesArr[i][0]);
            options.innerHTML = devicesArr[i][1];
            inputdevice.appendChild(options);
        }
        //
        //
        var inptgrp = document.createElement("DIV");
        inptgrp.setAttribute('class', 'input-group');
        inptgrp.setAttribute('style', 'margin-top: 5px');
        //
        var divbtns = document.createElement("DIV");
        divbtns.setAttribute('class', 'input-group-btn');
        divbtns.appendChild(btnremove);
        //
        //
        inptgrp.appendChild(inputdevice);
        inptgrp.appendChild(divbtns);
        //
        ////////////////////////////////
        //
        return inptgrp;
        //
        ////////////////////////////////
        //
    }

function createDvcpropsLGTV(roomNum, groupNum, deviceNum)
    {
        //
        ////////////////////////////////
        //
        var inputName = document.createElement("INPUT");
        inputName.setAttribute('id', 'name');
        inputName.setAttribute('type', 'text');
        inputName.setAttribute('class', 'form-control');
        inputName.setAttribute('placeholder', 'Enter device Name');
        //
        var inputIpaddress = document.createElement("INPUT");
        inputName.setAttribute('id', 'ipaddress');
        inputIpaddress.setAttribute('type', 'text');
        inputIpaddress.setAttribute('class', 'form-control');
        inputIpaddress.setAttribute('placeholder', 'Enter device IP Address');
        //
        var inputPrky = document.createElement("INPUT");
        inputName.setAttribute('id', 'pairingkey');
        inputPrky.setAttribute('type', 'text');
        inputPrky.setAttribute('class', 'form-control');
        inputPrky.setAttribute('placeholder', 'Enter device Pairing Key');
        //
        //
        var toggleTvguide = document.createElement("INPUT");
        inputName.setAttribute('id', 'usetvguide');
        toggleTvguide.setAttribute('type', 'checkbox');
        toggleTvguide.setAttribute('class', 'form-control');
        toggleTvguide.setAttribute('data-toggle', 'toggle');
        toggleTvguide.setAttribute('style', 'margin-right:20px;');
        toggleTvguide.setAttribute('data-on', 'Yes');
        toggleTvguide.setAttribute('data-off', 'No');
        //
        var lbl = document.createElement("H5");
        var tLbl = document.createTextNode("Use device for TV Guide ");
        var note = document.createElement("SMALL");
        var tNote = document.createTextNode(" (Only ONE device per group should have TV Guide use enabled)");
        lbl.appendChild(tLbl);
        note.appendChild(tLbl);
        lbl.appendChild(note);
        //
        //
        var div = document.createElement("DIV");
        div.setAttribute('style', 'margin-top: 5px');
        div.appendChild(inputName);
        div.appendChild(inputPrky);
        div.appendChild(inputIpaddress);
        div.appendChild(toggleTvguide);
        div.appendChild(lbl);
        //
        ////////////////////////////////
        //
        return div;
        //
        ////////////////////////////////
        //
    }

function createDvcpropsTIVO(roomNum, groupNum, deviceNum)
    {
        //
        ////////////////////////////////
        //
        var inputName = document.createElement("INPUT");
        inputName.setAttribute('id', 'name');
        inputName.setAttribute('type', 'text');
        inputName.setAttribute('class', 'form-control');
        inputName.setAttribute('placeholder', 'Enter device Name');
        //
        var inputIpaddress = document.createElement("INPUT");
        inputName.setAttribute('id', 'ipaddress');
        inputIpaddress.setAttribute('type', 'text');
        inputIpaddress.setAttribute('class', 'form-control');
        inputIpaddress.setAttribute('placeholder', 'Enter device IP Address');
        //
        var inputPrky = document.createElement("INPUT");
        inputName.setAttribute('id', 'mak');
        inputPrky.setAttribute('type', 'text');
        inputPrky.setAttribute('class', 'form-control');
        inputPrky.setAttribute('placeholder', 'Enter device Media Access Key');
        //
        //
        var toggleTvguide = document.createElement("INPUT");
        inputName.setAttribute('id', 'usetvguide');
        toggleTvguide.setAttribute('type', 'checkbox');
        toggleTvguide.setAttribute('class', 'form-control');
        toggleTvguide.setAttribute('data-toggle', 'toggle');
        toggleTvguide.setAttribute('style', 'margin-right:20px;');
        toggleTvguide.setAttribute('data-on', 'Yes');
        toggleTvguide.setAttribute('data-off', 'No');
        //
        var lbl = document.createElement("H5");
        var tLbl = document.createTextNode("Use device for TV Guide ");
        var note = document.createElement("SMALL");
        var tNote = document.createTextNode(" (Only ONE device per group should have TV Guide use enabled)");
        lbl.appendChild(tLbl);
        note.appendChild(tLbl);
        lbl.appendChild(note);
        //
        //
        var div = document.createElement("DIV");
        div.setAttribute('style', 'margin-top: 5px');
        div.appendChild(inputName);
        div.appendChild(inputPrky);
        div.appendChild(inputIpaddress);
        div.appendChild(toggleTvguide);
        div.appendChild(lbl);
        //
        ////////////////////////////////
        //
        return div;
        //
        ////////////////////////////////
        //
    }