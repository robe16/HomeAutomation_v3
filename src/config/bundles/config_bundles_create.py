from src.bundles.devices.tv_lg_netcast.tv_lg_netcast import device_tv_lg_netcast
from src.bundles.devices.tivo.tivo import device_tivo
from src.bundles.accounts.nest.nest import account_nest
from src.bundles.info_services.weather_metoffice.metoffice import info_metoffice

from src.config.bundles.config_bundles import get_cfg_bundles_json
from src.config.bundles.config_bundles import get_cfg_device_type, get_cfg_account_type
from src.log.console_messages import print_msg


def create_bundles(_devices, _accounts, _infoservices):
    #
    data = get_cfg_bundles_json()
    #
    for room_id in data['structure']['rooms']:
        #
        _devices[room_id] = {}
        room_devices = {}
        #
        for device_id in data['structure']['rooms'][room_id]['devices']:
            #
            room_devices[device_id] = _create_device(room_id, device_id)
            print_msg('Device object created: {type}: {room}:{device}'.format(type=get_cfg_device_type(room_id, device_id),
                                                                              room=room_id,
                                                                              device=device_id))
        _devices[room_id] = room_devices
    #
    for account_id in data['structure']['accounts']:
        #
        _accounts[account_id] = _create_account(account_id)
        print_msg('Account object created: {type}: {account}'.format(type=get_cfg_account_type(account_id),
                                                                     account=account_id))
    #
    _infoservices['weather'] = info_metoffice()
    print_msg('Infoservice object created: {type}'.format(type='weather'))
    #
    print_msg('All devices, accounts and infoservice instances created')


def _create_device(room_id, device_id):
    device_type = get_cfg_device_type(room_id, device_id)
    #
    if device_type=='tv_lg_netcast':
        return device_tv_lg_netcast(room_id=room_id, device_id=device_id)
    elif device_type=='tivo':
        return device_tivo(room_id=room_id, device_id=device_id)
    else:
        return False


def _create_account(account_id):
    device_type = get_cfg_account_type(account_id)
    #
    if device_type=='nest_account':
        return account_nest(account_id=account_id)
    else:
        return False