from config_devices_create import create_device_object

def cmd_fwrd(request):
    #
    dvc = create_device_object(request.query.group, request.query.device)
    #
    try:
        rsp = dvc.sendCmd(request)
        if isinstance(rsp, bool) and not isinstance(rsp, int):
            return True if bool(rsp) else False
        else:
            return rsp
    except:
        return False