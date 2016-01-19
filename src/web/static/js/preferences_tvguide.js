function buildList()
    {
        //
        errorFound = false;
        //
        var inptChans = document.getElementsByName('user-channel');
        //
        list = '[';
        //
        for (var i = 0; i < inptChans.length; i++)
            {
                //
                roomNum = i + 1;
                //
                if (inptChans[i].checked)
                    {
                        //
                        if (list=='[')
                            {list += '"' + inptChans[i].id + '"';}
                        else
                            {list += ', "' + inptChans[i].id + '"';}
                        //
                    }
                //
            }
        //
        list += ']'
        //
        return list;
        //
    }


function sendUpdate()
    {
    listChans = buildList();
    if (listChans)
        {
            sendHttp('/preferences/tvguide', listChans, 'POST', false, true);
            // TODO
            alert('Preferences sent to server');
        }
    else
        {
            alert('An error has ocurred, please try again.');
        }
    }