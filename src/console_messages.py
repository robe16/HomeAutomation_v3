from datetime import datetime


def print_command(command, device, ipaddress, response):
    print ("{ipaddress} - - [{timestamp}] - \'{command}\' request sent to {device} device - {response}").format(
        ipaddress=ipaddress,
        timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        command=command.replace('/r',''),
        device=device,
        response=response)
