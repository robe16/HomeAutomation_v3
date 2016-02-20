function sendNestCmd(group, device, command, value, nest_model, nest_device, nest_device_id) {
    //
    x = sendHttp('/command?group=' + group +
                '&device=' + device +
                '&command=' + command +
                '&value=' + value +
                '&nest_model=' + nest_model +
                '&nest_device=' + nest_device +
                '&nest_device_id=' + nest_device_id, null, 'GET', 1, true)
    //
    if (x) {
        document.getElementById('body').innerHTML = x;
    }
    //
}