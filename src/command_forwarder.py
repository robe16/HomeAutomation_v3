

def cmd_fwrd(arr_devices, request):
    #
    dvc = get_device(arr_devices, request.query.group, request.query.device)
    #
    try:
        rsp = dvc.sendCmd(request)
        if isinstance(rsp, bool):
            return True if bool(rsp) else False
        else:
            return rsp
    except:
        return False


def get_device(arr_devices, group_name, device_name):
    #
    for device_group in arr_devices:
        # Get group name - as some groups do not have a name, default this to '-'
        grp_name = '-' if device_group['name'] == '' else device_group['name']
        #
        if grp_name.lower().replace(' ', '') == group_name:
            #
            for objdevice in device_group['devices']:
                if objdevice.getLabel().lower().replace(' ', '') == device_name:
                    return objdevice
    return False