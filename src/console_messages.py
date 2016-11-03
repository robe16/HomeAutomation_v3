from datetime import datetime

timeformat = '%d/%m/%Y %H:%M:%S.%f'

def print_command(command, dvc_or_acc_id, device_type, dvc_ip, response):
    print ("{timestamp} - {dvc_or_acc_id} - \'{command}\' request sent to {device_type}{dvc_ip} - {response}".format(
        timestamp=datetime.now().strftime(timeformat),
        dvc_or_acc_id=dvc_or_acc_id,
        command=command.replace('/r',''),
        device_type=device_type,
        dvc_ip=' '+dvc_ip,
        response=response))


def print_channelbuild(num_current, num_total, name_chan):
    print ('{timestamp} - Building channels and retrieving TV Listing information: {current} out of {total} - {name}'
           .format(timestamp = datetime.now().strftime(timeformat),
                   current = num_current,
                   total = num_total,
                   name = name_chan))


def print_error(error_msg, dvc_or_acc_id=''):
    if (dvc_or_acc_id):
        dvc_or_acc_id += ' - '
    print ('{timestamp} - {dvc_or_acc_id}ERROR: {error}'.format(timestamp = datetime.now().strftime(timeformat),
                                                                dvc_or_acc_id=dvc_or_acc_id,
                                                                error = error_msg))


def print_http(httpcode, error_msg):
    print ('{timestamp} - HTTP {httpcode}: {error}'.format(timestamp = datetime.now().strftime(timeformat),
                                                           httpcode = httpcode,
                                                           error = error_msg))


def print_msg(msg, dvc_or_acc_id=''):
    if (dvc_or_acc_id):
        dvc_or_acc_id += ' - '
    print ('{timestamp} - {dvc_or_acc_id}{msg}'.format(timestamp=datetime.now().strftime(timeformat),
                                                       dvc_or_acc_id=dvc_or_acc_id,
                                                       msg=msg))