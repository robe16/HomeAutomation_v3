from urllib import urlopen
from web_menu import html_menu
from web_tvlistings import html_listings_user_and_all


def _html_build_device_panels (device, group):
    device_url = "device/{}/{}".format(group, device.getName().replace(" ", "")).lower()
    if device.getLogo:
        str_panel = "<img src=\"/img/logo/{}\" style=\"height:25px;\"/> {}".format(device.getLogo(),
                                                                                   device.getName())
    else:
        str_panel = device.getName()
    str_objhtml = urlopen(('web/{}').format(device.getHtml())).read().encode('utf-8').format(url=device_url)
    str_devicehtml = urlopen('web/comp_panel.html').read().encode('utf-8').format(title=str_panel,
                                                                                   body=str_objhtml)
    str_devicehtml += "<br>"
    return str_devicehtml


def _html_device_inputsandoutputs(devices, group):
    #
    if len(devices)>1:
        count = 1
        html_pills = '<ul class="nav nav-pills nav-justified">'
        html_pills_content = '<div class="tab-content">'
        #
        for device in devices:
            #
            dvc = device['device']
            active_pill = ' class="active"' if count==1 else ''
            active_contents = ' active' if count==1 else ''
            #
            html_pills += ('<li role="presentation"{active}>' +
                              '<a data-toggle="pill" href="#pill_{href}">{name}</a>' +
                              '</li>').format(active=active_pill,
                                              href=dvc.getName().lower().replace(' ',''),
                                              name=dvc.getName())
            html_panel = _html_build_device_panels(dvc, group)
            html_pills_content += ('<div id="pill_{href}" class="tab-pane fade in{active}">' +
                                  '{pill_panels}' +
                                  '</div>').format(href=dvc.getName().lower().replace(' ',''),
                                                   active=active_contents,
                                                   pill_panels=html_panel)
            count += 1
        #
        html_pills += '</ul><br/>'
        html_pills_content += '</div>'
        #
        return html_pills + html_pills_content
        #
    elif len(devices)==1:
        for dvc in devices:
            return _html_build_device_panels(dvc, group)
        return
    else:
        return ''



def create_device_page(user, tvlistings, arr_objects, group):
    #
    html_body = ""
    #
    for devicegroup in arr_objects:
        if devicegroup['name'].lower().replace(' ','') == group:
            device = devicegroup['devices']['device']
            #
            html_device = _html_build_device_panels (device, group)
            html_input = _html_device_inputsandoutputs(devicegroup['devices']['inputs'], group)
            html_output = _html_device_inputsandoutputs(devicegroup['devices']['outputs'], group)
            #
            html_devices = html_output + html_device + html_input
            #
            #device_url = "device/{group}/{device}".format(group=group, device=list_objects[x].getName().replace(" ", "")).lower()
            device_url = ''
            chan_current = ''
            #
            #TODO
            if devicegroup['tvguide']:
                #html_tvguide = html_listings_user_and_all (tvlistings,
                #                                           group=group,
                #                                           device_url=device_url,
                #                                           device=device,
                #                                           chan_current=chan_current,
                #                                           user=user)
                html_tvguide = html_listings_user_and_all (tvlistings,
                                                           chan_current=chan_current,
                                                           user=user)
                #
                html_body = urlopen('web/group_with-tvguide.html').read().encode('utf-8').format(group=group,
                                                                                                 devices=html_devices,
                                                                                                 tvguide=html_tvguide)
            else:
                html_body = urlopen('web/group_no-tvguide.html').read().encode('utf-8').format(group=group,
                                                                                               devices=html_devices)
            #
    return urlopen('web/header.html').read().encode('utf-8') + \
           html_menu(user) + \
           urlopen('web/comp_alert.html').read().encode('utf-8').format(body="-") + \
           html_body + \
           urlopen('web/footer.html').read().encode('utf-8')
    #


#from config_devices import create_device_object_array
#create_device_page("Rob", None, create_device_object_array(), "Lounge TV")
#print ('done')