from datetime import datetime

timeformat = '%d/%m/%Y %H:%M:%S.%f'

def print_command(command, device, ipaddress, response):
    print ("{timestamp} - \'{command}\' request sent to {device} device {ipaddress} - {response}").format(
        ipaddress=ipaddress,
        timestamp=datetime.now().strftime(timeformat),
        command=command.replace('/r',''),
        device=device,
        response=response)


def print_channelbuild(num_current, num_total, name_chan):
    print ('{timestamp} - Building channels and retrieving TV Listing information: {current} out of {total} - {name}'
           .format(timestamp = datetime.now().strftime(timeformat),
                   current = num_current,
                   total = num_total,
                   name = name_chan))

def print_error(error_msg):
    print ('{timestamp} - ERROR: {error}'.format(timestamp = datetime.now().strftime(timeformat),
                                                 error = error_msg))

def print_http(httpcode, error_msg):
    print ('{timestamp} - HTTP {httpcode}: {error}'.format(timestamp = datetime.now().strftime(timeformat),
                                                           httpcode = httpcode,
                                                           error = error_msg))

def print_msg(msg):
    print ('{timestamp} - {msg}'.format(timestamp = datetime.now().strftime(timeformat),
                                        msg = msg))