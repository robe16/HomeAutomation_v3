from bindings.tv_lg_netcast.tv_lg_netcast import device_tv_lg_netcast
from bindings.tivo.tivo import device_tivo
from bindings.nest.nest import account_nest
from bindings.news.news import info_news
from bindings.weather.weather import info_metoffice
from bindings.tvlistings.tvlistings import info_tvlistings

from config.bindings.config_bindings import get_cfg_bindings_json
from log.log import log_error, log_general


def create_bindings(_things, _infoservices):
    #
    data = get_cfg_bindings_json()
    #
    for group in data['bindings']['groups']:
        #
        _things[group['sequence']] = {}
        group_things = {}
        #
        for thing in group['things']:
            #
            try:
                group_things[thing['sequence']] = _create_thing(thing['type'], group['sequence'], thing['sequence'])
                log_general('Thing created: {type}: {group}:{thing}'.format(type=thing['type'],
                                                                            group=group['name'],
                                                                            thing=thing['name']))
            except Exception as e:
                log_error('Coud not create Thing: {type}: {group}:{thing}'.format(type=thing['type'],
                                                                                  group=group['name'],
                                                                                  thing=thing['name']))
            #
        #
        _things[group['sequence']] = group_things
        #
    #
    for info in data['bindings']['info_services']:
        #
        try:
            _infoservices[info['sequence']] = _create_info(info['type'], info['sequence'])
            log_general('Info_service created: {type}: {info}'.format(type=info['type'],
                                                                      info=info['name']))
        except Exception as e:
            log_error('Coud not create Info_service: {type}: {info}'.format(type=info['type'],
                                                                            info=info['name']))
        #
    #
    log_general('All instances of Things and Info_services created')


def _create_thing(thing_type, group_seq, thing_seq):
    #
    if thing_type=='tv_lg_netcast':
        return device_tv_lg_netcast(group_seq, thing_seq)
    elif thing_type=='tivo':
        return device_tivo(group_seq, thing_seq)
    elif thing_type=='nest_account':
        return account_nest(group_seq, thing_seq)
    else:
        return False


def _create_info(thing_type, info_seq):
    #
    if thing_type=='weather':
        return info_metoffice(info_seq)
    elif thing_type=='tvlistings':
        return info_tvlistings(info_seq)
    elif thing_type=='news':
        return info_news(info_seq)
    else:
        return False