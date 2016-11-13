from urllib import urlopen

from src.config.devices.config_devices import get_cfg_device_json
from src.lists.devices.list_devices import read_list_devices, get_device_name, get_device_logo


#TODO - needs completely rewriting!!
def settings_devices():
    #
    html_groups = ''
    grp_num = 0
    #
    data = get_cfg_device_json()
    #
    grp_keys = data.keys()
    for grp in grp_keys:
        #
        html_devices = ''
        dvc_num = 0
        #
        dvc_keys = data[grp]['devices'].keys()
        for dvc in dvc_keys:
            try:
                raise Exception
                #TODO
                #device = create_device_object(grp, dvc)
                html_devices += device.getHtml_settings(grp_num, dvc_num)
            except Exception as e:
                html_devices += ''
            dvc_num += 1
        #
        html_groups += settings_devices_group(grp_num,
                                              dvcnum=dvc_num,
                                              group_name=data[grp]['group'],
                                              devices=html_devices)
        grp_num += 1
    #
    return urlopen('web/html_settings/settings_devices.html').read().encode('utf-8').format(groups = html_groups,
                                                                                            grpnum = str(grp_num))

def settings_devices_selection(grpnum, dvcnum):
    #
    body = '<div class="row">'
    count = 0
    devices = read_list_devices()
    #
    device_keys = devices.keys()
    #
    for dvc_key in device_keys:
        if count> 0 and count % 4 == 0:
            body += '</div><div class="row">'
        #
        name = get_device_name(devices[dvc_key]['type'])
        img = get_device_logo(devices[dvc_key]['type'])
        #
        body += urlopen('web/html_settings/settings_devices_selection_item.html').read().encode('utf-8').format(name=name,
                                                                                                                img=img,
                                                                                                                grpnum=grpnum,
                                                                                                                dvcnum=dvcnum,
                                                                                                                type=devices[dvc_key]['type'].lower().replace(' ',''))
        count += 1
    #
    body += '</div>'
    #
    return body


def settings_devices_group(grpnum, dvcnum, group_name = '', devices = ''):
    #
    return urlopen('web/html_settings/settings_devices_group.html').read().encode('utf-8').format(group_name=group_name,
                                                                                                  devices=devices,
                                                                                                  grpnum=str(grpnum),
                                                                                                  dvcnum=str(dvcnum),
                                                                                                  grp_ref='grp'+str(grpnum))