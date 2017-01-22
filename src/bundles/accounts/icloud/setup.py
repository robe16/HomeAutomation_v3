import sys
import datetime
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException

_dateformat = '%d/%m/%Y %H:%M:%S'

def setup_icloud():
    #
    name = raw_input("Enter the name: ")
    username = raw_input("Username: ")
    password = raw_input("Password: ")
    #
    try:
        #
        api = PyiCloudService(username, password)
        #
        twofactor_choice = ''
        twofactor_timestamp = ''
        #
        if api.requires_2fa:
            import click
            print("Two-factor authentication required. Your trusted devices are:")

            devices = api.trusted_devices
            for i, device in enumerate(devices):
                print "  %s: %s" % (i, device.get('deviceName',
                                                  "SMS to %s" % device.get('phoneNumber')))

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not api.send_verification_code(device):
                print("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not api.validate_verification_code(device, code):
                print("Failed to verify verification code")
                sys.exit(1)
            #
            twofactor_choice = device
            twofactor_timestamp = datetime.datetime.now().strftime(_dateformat)
            #
        #
    except PyiCloudFailedLoginException:
        print("\n!! Username/password combination is incorrect - please try again !!")
        print("\n****************************************************************\n")
        return
    except:
        print("\n!! An error has ocurred - please try again !!")
        print("\n****************************************************************\n")
        return
    #
    new_acc = {}
    new_acc['account_type'] = 'icloud_account'
    new_acc['account_name'] = name
    new_acc['account_id'] = name.lower().replace(' ', '_').replace('\'', '')
    new_acc['details'] = {'username': username,
                          'password': password,
                          '2factor': {'2factor_required': api.requires_2fa,
                                      '2factor_choice': twofactor_choice,
                                      '2factor_timestamp': twofactor_timestamp}}
    new_acc['details_public'] = {}
    #
    return new_acc
