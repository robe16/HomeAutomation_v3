from urllib import urlopen
from list_devices import read_list_devices, get_device_name, get_device_logo


def settings_devices(arr_devices):
    # TODO - code to create entire page to reflect json config file
    #
    html_groups =''
    grp_num = 0
    #
    for device_group in arr_devices:
        #
        html_devices = ''
        #
        for device in device_group['devices']:
            try:
                html_devices += device.getHtml_settings()
            except:
                html_devices += ''
        #
        html_groups += settings_devices_group(grp_num,
                                              group_name = device_group['name'],
                                              devices = html_devices)
        grp_num += 1
    #
    return urlopen('web/html_settings/settings_devices.html').read().encode('utf-8').format(groups = html_groups,
                                                                                            num = str(0))

def settings_devices_selection(grpnum):
    #
    body = '<div class="row">'
    count = 0
    devices = read_list_devices()
    #
    for dvc in devices:
        if count> 0 and count % 4 == 0:
            body += '</div><div class="row">'
        #
        name = get_device_name(dvc['type'])
        img = get_device_logo(dvc['type'])
        #
        body += urlopen('web/html_settings/settings_devices_selection_item.html').read().encode('utf-8').format(name = name,
                                                                                                                img = img,
                                                                                                                grpnum = grpnum,
                                                                                                                type = dvc['type'].lower().replace(' ',''))
        count += 1
    #
    body += '</div>'
    #
    return body


def settings_devices_group(num, group_name = '', devices = ''):
    #
    return urlopen('web/html_settings/settings_devices_group.html').read().encode('utf-8').format(group_name=group_name,
                                                                                                  devices=devices,
                                                                                                  num=str(num))