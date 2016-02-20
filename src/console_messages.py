from datetime import datetime


def print_command(command, device, ipaddress, response):
    print ("{timestamp} - \'{command}\' request sent to {device} device {ipaddress} - {response}").format(
        ipaddress=ipaddress,
        timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        command=command.replace('/r',''),
        device=device,
        response=response)


def print_channelbuild(num_current, num_total, name_chan):
    print ('{timestamp} - Building channels and retrieving TV Listing information: {current} out of {total} - {name}'
           .format(timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                   current = num_current,
                   total = num_total,
                   name = name_chan))

def print_error(error_msg):
    print ('{timestamp} - ERROR: {error}'.format(timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                 error = error_msg))

def print_http(httpcode, error_msg):
    print ('{timestamp} - HTTP {httpcode}: {error}'.format(timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                                           httpcode = httpcode,
                                                           error = error_msg))